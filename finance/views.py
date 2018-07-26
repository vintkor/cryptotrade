from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from .models import UsersFinanceHistory, Purpose
from .forms import (
    SendMoneyForm,
)
from user_profile.models import User
from .utils import set_transaction_to_finance_history, make_uuid
from django.db.transaction import atomic
import decimal
from django.contrib import messages
from django.utils.translation import ugettext as _


class FinanceHistoryListView(LoginRequiredMixin, ListView):
    template_name = 'finance/user-finance-history.html'
    context_object_name = 'finances'
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        return UsersFinanceHistory.objects.filter(user=self.request.user)


class SendMoneyFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('user:login')
    form_class = SendMoneyForm
    template_name = 'finance/send-money.html'

    def post(self, request, *args, **kwargs):
        unique_number = self.request.POST.get('recipient_js')

        if unique_number:
            try:
                user = User.objects.get(unique_number=unique_number)
            except User.DoesNotExist:
                return JsonResponse({
                    'status': False,
                })

            return JsonResponse({
                'status': True,
                'recipient': user.get_full_name(),
            })

        return super(SendMoneyFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        user_recipient = get_object_or_404(User, unique_number=form.cleaned_data['recipient'])
        sender = self.request.user
        uuid = make_uuid()

        if sender.balance < decimal.Decimal(amount):
            messages.error(self.request, _('У вас недостаточно средств'), 'danger')
            return redirect(self.request.META.get('HTTP_REFERER'))

        with atomic():
            sender.balance = sender.balance - decimal.Decimal(amount)
            sender.save(update_fields=('balance',))

            user_recipient.balance = user_recipient.balance - decimal.Decimal(amount)
            user_recipient.save(update_fields=('balance',))

            sender_purpose = Purpose.objects.get(code=14)
            recipient_purpose = Purpose.objects.get(code=15)

            set_transaction_to_finance_history(
                amount=decimal.Decimal(amount),
                sender_id=sender.id,
                recipient_id=user_recipient.id,
                sender_purpose_id=sender_purpose.id,
                recipient_purpose_id=recipient_purpose.id,
                uuid=uuid
            )

        messages.success(self.request, _('Перевод был отправлен успешно'))
        return redirect(reverse_lazy('finance:finance-history'))
