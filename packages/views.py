from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from .models import Package, PackageHistory
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.db.transaction import atomic
from django.utils.crypto import get_random_string
from finance.utils import set_transaction_to_finance_history, make_uuid
from user_profile.models import User
from finance.models import Purpose
from binary_tree.utils import SetPoints
from shares.models import ShareHolder, Course
from awards.utils import start_rang_award_runner
from cryptotrade.settings import NOT_VERIFIED_MESSAGE


class PackageListView(LoginRequiredMixin, ListView):
    template_name = 'packages/packages-list.html'
    context_object_name = 'packages'
    model = Package
    login_url = reverse_lazy('user:login')


class ByPackageFormView(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')
    permission_required = ['user_profile.is_verified']

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_VERIFIED_MESSAGE), 'danger')
        return super(ByPackageFormView, self).handle_no_permission()

    def post(self, request, package_id):
        package = get_object_or_404(Package, pk=package_id)
        user = self.request.user

        if user.balance < package.price:
            messages.error(request, _('На Вашем счету недостаточно средств. Вам необходимо пополнить баланс.'), 'danger')
            return redirect(self.request.META['HTTP_REFERER'])

        amount = package.make_price_for_user(user)
        balance = user.balance - amount
        old_package = user.package
        amount_tokens = package.make_tokens_for_user(user)
        amount_points = package.make_points_for_user(user)

        try:
            system_balance = User.objects.get(login='SYSTEM_BALANCE')
        except User.DoesNotExist:
            raise ValueError(_('Необходимо создать пользователя с логином SYSTEM_BALANCE'))

        sender_purpose = Purpose.objects.get(code=10)
        recipient_purpose = Purpose.objects.get(code=11)
        uuid = make_uuid()

        with atomic():
            user.package = package
            user.set_status_active()
            user.balance = balance
            user.volume += amount
            user.save(update_fields=('package', 'status', 'balance', 'volume',))

            package_history = PackageHistory(
                user=user,
                old_package=old_package,
                package=package,
                uuid=get_random_string(60),
            )
            package_history.save()

            set_transaction_to_finance_history(
                amount=amount,
                sender_id=user.id,
                recipient_id=system_balance.id,
                sender_purpose_id=sender_purpose.id,
                recipient_purpose_id=recipient_purpose.id,
                uuid=uuid,
            )

            share_holder = ShareHolder(
                user=user,
                amount=amount_tokens,
                course=Course.get_last_course(),
            )
            share_holder.save()

            system_balance.balance += amount
            system_balance.save(update_fields=('balance',))

            set_points = SetPoints(user.id, amount_points)
            set_points.set_points()

            messages.success(request, _('Пакет успешно куплен.'))

        start_rang_award_runner()

        # TODO проверить полное ли заполнение

        return redirect(self.request.META['HTTP_REFERER'])
