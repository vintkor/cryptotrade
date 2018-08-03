from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, View
from .models import (
    UsersFinanceHistory,
    Purpose,
    PaymentSystem,
    PaymentHistory,
)
from .forms import (
    SendMoneyForm,
)
from user_profile.models import User
from .utils import set_transaction_to_finance_history, make_uuid
from django.db.transaction import atomic
import decimal
from django.contrib import messages
from django.utils.translation import ugettext as _
from .payments_utils.payeer import Payeer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from hashlib import sha256


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
            sender.balance -= decimal.Decimal(amount)
            sender.save(update_fields=('balance',))

            user_recipient.balance += decimal.Decimal(amount)
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


class AddMoneyBaseView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('user:login')
    template_name = 'finance/add-money-base-view.html'
    queryset = PaymentSystem.objects.filter(is_active=True)
    context_object_name = 'payment_systems'

    def post(self, request):
        payment_system_id = request.POST.get('payment_system_id')
        amount = request.POST.get('amount')

        try:
            ps = PaymentSystem.objects.get(id=payment_system_id)
        except PaymentSystem.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': _('Платёжной системы не существует')
            })

        ph = PaymentHistory(
            user=self.request.user,
            payment_system=ps,
            amount=decimal.Decimal(amount),
        )
        ph.save()

        if ps.title == 'Payeer':
            payeer = Payeer(
                m_amount=amount,
                m_curr='USD',
                m_desc='Пополнение баланса пользователя {}'.format(self.request.user.unique_number),
                m_shop=ps.settings.get('m_shop'),
                m_orderid=ph.pk,
                m_key=ps.settings.get('m_key'),
                button_text=_('Перейти на страницу оплаты'),
            )
            merchant_form = payeer.get_merchant_form()

            return JsonResponse({
                'status': True,
                'merchant_form': merchant_form,
            })

        return JsonResponse({
            'status': False,
            'message': _('Неверный запрос')
        })


@method_decorator(csrf_exempt, name='dispatch')
class PayeerFailView(View):

    def get(self, request):
        messages.error(request, _('Пополнить счёт не удалось'), 'danger')
        return redirect(reverse_lazy('finance:add-money'))


@method_decorator(csrf_exempt, name='dispatch')
class PayeerStatusView(View):

    def post(self, request):
        ps = ps = PaymentSystem.objects.get(code=110)
        print('-'*80)
        response_for_payeer = 'error'

        if request.POST.get('m_operation_id', None) and request.POST.get('m_sign', None):

            m_operation_id = request.POST.get('m_operation_id')
            m_operation_ps = request.POST.get('m_operation_ps')
            m_operation_date = request.POST.get('m_operation_date')
            m_operation_pay_date = request.POST.get('m_operation_pay_date')
            m_shop = request.POST.get('m_shop')
            m_orderid = request.POST.get('m_orderid')
            m_amount = request.POST.get('m_amount')
            m_curr = request.POST.get('m_curr')
            m_desc = request.POST.get('m_desc')
            m_status = request.POST.get('m_status')
            m_key = ps.settings.get('m_key')

            result_string = "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(m_operation_id, m_operation_ps, m_operation_date,
                                                                      m_operation_pay_date,
                                                                      m_shop, m_orderid, m_amount, m_curr, m_desc,
                                                                      m_status, m_key)

            sign_hash = sha256(result_string.encode())
            sing = sign_hash.hexdigest().upper()

            amount = decimal.Decimal(m_amount)

            # Совпадает сумма и прошла ли оплата
            if request.POST.get('m_sign') == sing and request.POST.get('m_status') == 'success':

                try:
                    ph = PaymentHistory.objects.get(id=int(m_orderid))
                except PaymentHistory.DoesNotExist:
                    response_for_payeer = m_orderid + "|error"
                    return HttpResponse(response_for_payeer)

                if ph.amount == amount:
                    with atomic():
                        user = ph.user
                        user.balance += amount
                        user.save(update_fields=('balance',))

                        ph.is_success = True
                        ph.save(update_fields=('is_success',))

                        sender_purpose = Purpose.objects.get(code=18)
                        recipient_purpose = Purpose.objects.get(code=19)

                        uuid = make_uuid()
                        set_transaction_to_finance_history(
                            amount=amount,
                            recipient_id=user.id,
                            sender_purpose_id=sender_purpose.id,
                            recipient_purpose_id=recipient_purpose.id,
                            uuid=uuid,
                        )

                    response_for_payeer = m_orderid + "|success"
                else:
                    response_for_payeer = m_orderid + "|error"
            else:
                response_for_payeer = m_orderid + "|error"

        return HttpResponse(response_for_payeer)


@method_decorator(csrf_exempt, name='dispatch')
class PayeerSucceessView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def post(self, request):
        return redirect(reverse_lazy('finance:finance-history'))
