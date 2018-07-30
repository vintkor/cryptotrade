from django import forms
from django.forms import Form
from geo.models import Country
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from .models import User


names_validator = validators.RegexValidator('^[a-zA-Zа-яА-Я]+$', message=_(
        'Допускаются только латинские и кирилические символы нижнего и верхнего регистра'
    ))

phone_validator = validators.RegexValidator('^[0-9]+')
password_validator = validators.MinLengthValidator(10)


class RegistrationByRefCodeForm(forms.Form):
    """
    Форма регистрации пользователя по реферальной ссылке
    """
    error_css_class = 'is-invalid'
    errors_class = 'is-invalid'

    login = forms.CharField(label=_('Логин'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[validators.RegexValidator('^[a-zA-Z0-9-_#$%]+$', message=_(
        'Допускаются только латинские символы нижнего и верхнего регистра, а также спецсимволы #-_$'
    ))])
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[validators.EmailValidator])
    first_name = forms.CharField(label=_('Имя'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[names_validator])
    last_name = forms.CharField(label=_('Фамилия'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[names_validator])
    country = forms.ModelChoiceField(label=_('Страна'), queryset=Country.objects.filter(is_active=True), widget=forms.Select(
        attrs={'class': 'form-control select2'}
    ), required=True, help_text=_('Если вы не нашли своей страны в списке, значит для вас регистрация запрещена!'))
    phone = forms.CharField(label=_('Номер телефона'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[phone_validator], help_text=_('Номер телефона должен быть в международном формате но без знака +'))
    password = forms.CharField(label=_('Пароль'), widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), validators=[password_validator])
    repeat_password = forms.CharField(label=_('Пароль ещё раз'), widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        super(RegistrationByRefCodeForm, self).__init__(*args, **kwargs)
        self.fields['parent'] = forms.CharField(widget=forms.TextInput(
            attrs={'value': parent.ref_code, 'type': 'hidden'}
        ))

    def get_repeat_pass(self):
        return self.data.get('repeat_password')

    def clean_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.get_repeat_pass()

        if repeat_password != password:
            raise forms.ValidationError(_('Пароли не совпадают'), code='invalid')

        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('Такой номер телефона уже используется'))
        else:
            return phone


class AuthForm(Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'email'}), validators=[validators.EmailValidator])

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))


class VerificationForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Имя'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[names_validator])
    last_name = forms.CharField(label=_('Фамилия'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[names_validator])
    email = forms.EmailField(label=_('Email'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[validators.EmailValidator])
    country = forms.ModelChoiceField(label=_('Страна'), queryset=Country.objects.filter(is_active=True),
                                     widget=forms.Select(
                                         attrs={'class': 'form-control select2'}
                                     ), required=True, help_text=_(
            'Если вы не нашли своей страны в списке, значит для вас регистрация запрещена!'))
    phone = forms.CharField(label=_('Номер телефона'), widget=forms.TextInput(
        attrs={'class': 'form-control'},
    ), validators=[phone_validator])

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'country',
        )
