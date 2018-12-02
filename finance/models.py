from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import User
from django.contrib.postgres.fields import JSONField
import datetime
from cryptotrade.settings import BLOCKIO_TIME
from django.db.transaction import atomic


class Purpose(models.Model):
    """
    Назначения платежей
    """
    code = models.PositiveSmallIntegerField(verbose_name=_('Код платежа'), unique=True)
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))

    class Meta:
        verbose_name_plural = _('Назначения платежей')
        verbose_name = _('Назначение платежа')
        ordering = ('-code',)

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

    @staticmethod
    def set_new_operation(user, amount, purpose, uuid, second_user=None):
        history = UsersFinanceHistory()
        history.user = user
        history.amount = amount
        history.purpose = purpose
        if second_user:
            history.second_user = second_user
        history.uuid = uuid
        history.save()


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


MONEY_REQUEST_STATUSES = (
    ('1', _('Новый')),
    ('2', _('Отказано')),
    ('3', _('Выполнен')),
)


class MoneyRequest(models.Model):
    """
    Запросы на вывод средств
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    amount = models.DecimalField(verbose_name=_('Сумма'), max_digits=13, decimal_places=2)
    info = models.TextField(verbose_name=_('Дополнительная информация'), blank=True, null=True)
    status = models.CharField(verbose_name=_('Статус'), choices=MONEY_REQUEST_STATUSES, max_length=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Запрос на вывод средств')
        verbose_name_plural = _('Запросы на вывод средств')
        permissions = (
            ("can_moderate_money_requests", "Может модерировать вывод средств"),
        )
        ordering = ('-id',)

    def __init__(self, *args, **kwargs):
        super(MoneyRequest, self).__init__(*args, **kwargs)
        self._old_status = self.status

    def __str__(self):
        return '{} -> {}'.format(self.user.unique_number, self.amount)

    def save(self, *args, **kwargs):
        if self._old_status != self.status:

            if self.status_is_done():
                self.save_money_transaction(is_done=True)

            if self.status_is_denied():
                self.save_money_transaction(is_denied=True)

        return super(MoneyRequest, self).save(*args, **kwargs)

    def status_is_new(self):
        if self.status == MONEY_REQUEST_STATUSES[0][0]:
            return True
        return False

    def status_is_denied(self):
        if self.status == MONEY_REQUEST_STATUSES[1][0]:
            return True
        return False

    def status_is_done(self):
        if self.status == MONEY_REQUEST_STATUSES[2][0]:
            return True
        return False

    @property
    def status_class(self):
        if self.status_is_new():
            return 'info'
        if self.status_is_done():
            return 'success'
        else:
            return 'danger'

    def save_money_transaction(self, is_denied=False, is_done=False):
        self.user.update_freeze_balance(-self.amount)

        if is_done:
            purpose_for_user = Purpose.objects.get(code=26)
            from finance.utils import make_uuid
            uuid = make_uuid()

            with atomic():
                self.user.save()
                UsersFinanceHistory.set_new_operation(
                    user=self.user,
                    amount=-self.amount,
                    purpose=purpose_for_user,
                    uuid=uuid,
                )

        if is_denied:
            with atomic():
                self.user.update_balance(self.amount)
                self.user.save()
