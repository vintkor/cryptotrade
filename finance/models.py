from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import User
from django.contrib.postgres.fields import JSONField
import datetime
from cryptotrade.settings import BLOCKIO_TIME


class Purpose(models.Model):
    """
    Назначения платежей
    """
    code = models.PositiveSmallIntegerField(verbose_name=_('Код платежа'), unique=True)
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))

    class Meta:
        verbose_name_plural = _('Назначения платежей')
        verbose_name = _('Назначение платежа')

    def __str__(self):
        return self.title


class UsersFinanceHistory(models.Model):
    """
    Финансовая история
    """
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(verbose_name=_('Сумма'), max_digits=12, decimal_places=2)
    purpose = models.ForeignKey(Purpose, verbose_name=_('Назначение платежа'), on_delete=models.CASCADE)
    second_user = models.ForeignKey(
        User, related_name='second_user', verbose_name=_('Второй пользователь'),
        on_delete=models.CASCADE, blank=True, null=True
    )
    uuid = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name_plural = _('Финансы пользователя')
        verbose_name = _('Финансы пользователей')
        ordering = ('-id',)

    def __str__(self):
        return "{}".format(self.user)

    def get_number(self):
        return self.user.unique_number if self.user else '---'

    get_number.short_description = _('Пользователь')

    def get_number_second_user(self):
        if self.second_user:
            return self.second_user.unique_number
        return '---'

    get_number_second_user.short_description = _('Второй пользователь')


class PaymentSystem(models.Model):
    """
    Платёжные системы
    """
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    code = models.PositiveIntegerField(unique=True, verbose_name=_('Уникальный код системы'))
    logo = models.ImageField(verbose_name=_('Логотип'), upload_to='payment-systems', blank=True, null=True)
    settings = JSONField(verbose_name=_('Настройки системы'), blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('Является активной'), default=False)

    class Meta:
        verbose_name = _('Платёжная система')
        verbose_name_plural = _('Платёжные системы')

    def __str__(self):
        return self.title


class PaymentHistory(models.Model):
    """
    История платежей
    """
    user = models.ForeignKey('user_profile.User', verbose_name=_('Пользователь'), max_length=20, on_delete=models.CASCADE)
    payment_system = models.ForeignKey(PaymentSystem, verbose_name=_('Платёжная система'), on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name=_('Сумма'), decimal_places=2, max_digits=10)
    is_success = models.BooleanField(verbose_name=_('Является успешной'), default=False)
    info = JSONField(verbose_name=_('Дополнительная информация'), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('История платежей')
        verbose_name_plural = _('Истории платежей')

    def __str__(self):
        return str(self.amount)


class BlockIOWallet(models.Model):
    """
    Кошельки пользователей для пополнения баланса в системе через сервис Block.io
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    wallet = models.CharField(max_length=200, verbose_name=_('Кошелёк'))
    currency = models.ForeignKey(PaymentSystem, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=30, decimal_places=12, default=0)
    balance_usd = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))
    end_date = models.DateTimeField(verbose_name=_('Дата создания'), blank=True, null=True)
    is_done = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Кошелёк пользователя')
        verbose_name_plural = _('Bitcoin кошелёки пользователей')

    def __str__(self):
        return self.user.unique_number

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = datetime.datetime.now() + datetime.timedelta(seconds=BLOCKIO_TIME)            
        return super(BlockIOWallet, self).save(*args, **kwargs)
