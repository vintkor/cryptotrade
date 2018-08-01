from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import User
from colorfield.fields import ColorField


class Package(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    price = models.DecimalField(verbose_name=_('Цена'), decimal_places=2, max_digits=7)
    tokens = models.PositiveIntegerField(verbose_name=_('Токены'))
    points = models.PositiveIntegerField(verbose_name=_('Баллы'))
    bonuses = models.PositiveIntegerField(verbose_name=_('Бонусы'))
    weight = models.PositiveSmallIntegerField(verbose_name=_('Вес'), default=1)
    color = ColorField(default='#000000', verbose_name=_('Цвет пакета'))

    class Meta:
        verbose_name = _('Пакет')
        verbose_name_plural = _('Пакеты')
        ordering = ('weight',)

    def __str__(self):
        return self.title

    def make_price_for_user(self, user):
        if user.package:
            return self.price - user.package.price
        return self.price

    def make_tokens_for_user(self, user):
        if user.package:
            return self.tokens - user.package.tokens
        return self.tokens

    def make_points_for_user(self, user):
        if user.package:
            return self.points - user.package.points
        return self.points


class PackageHistory(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    old_package = models.ForeignKey(Package, verbose_name=_('Предыдущий пакет'), default=None, blank=True,
                                    null=True, related_name='old_pakcage', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, verbose_name=_('Пакет'), on_delete=models.CASCADE)
    uuid = models.CharField(max_length=60, default=None, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('История покупки пакетов')
        verbose_name_plural = _('Истории покупки пакетов')

    def __str__(self):
        return '{} > {}'.format(self.user.unique_number, self.package)
