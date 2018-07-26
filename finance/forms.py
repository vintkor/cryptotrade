from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core import validators
import decimal


recipient_validator = validators.RegexValidator('CT-[0-9]{7}', message=_(
        'Неверно указан получатель'
    ))


class SendMoneyForm(forms.Form):
    recipient = forms.CharField(label=_('Получатель'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'CT-1000002'},
    ), validators=[recipient_validator])
    amount = forms.CharField(label=_('Сумма'), widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'number', 'min': 1, 'step': .1, 'value': 10},
    ))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if decimal.Decimal(amount) < 1:
            raise ValueError(_('Сумма не может быть 0 и меньше'))
        return amount
