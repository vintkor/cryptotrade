from django.db import models
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField


class RangAward(models.Model):
    title = models.CharField(verbose_name=_('Заголовок'), max_length=60)
    volume = models.DecimalField(verbose_name=_('Объём'), max_digits=10, decimal_places=2)
    max_lines = models.PositiveSmallIntegerField(verbose_name=_('Количество линий'))
    lines_volume = models.DecimalField(verbose_name=_('Объём в линиях'), max_digits=10, decimal_places=2)
    include_rang = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('Ранг партнёров'), null=True, blank=True)
    include_rang_count = models.PositiveSmallIntegerField(verbose_name=_('Количество партнёров с указаным рангом'))
    bonus = models.DecimalField(verbose_name=_('Бонус'), max_digits=10, decimal_places=2)
    is_final = models.BooleanField(default=False)
    is_start = models.BooleanField(default=False)
    quick_days = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('К-во дней с момента регистрации'))
    quick_bonus = models.DecimalField(blank=True, null=True, verbose_name=_('Бонус быстрого старта'), decimal_places=2, max_digits=10)
    weight = models.PositiveSmallIntegerField(default=10, verbose_name=_('Вес'))

    class Meta:
        verbose_name = _('Ранговый бонус')
        verbose_name_plural = _('Ранговые бонусы')
        ordering = ('volume',)

    def __str__(self):
        return self.title


class RangAwardHistory(models.Model):
    user = models.ForeignKey('user_profile.User', on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    text = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('История начисления рангового бонуса')
        verbose_name_plural = _('Истории начисления рангового бонуса')

    def __str__(self):
        return self.user.unique_number


class MultiLevelBonus(models.Model):
    rang = models.ForeignKey(RangAward, on_delete=models.CASCADE, verbose_name=_('Ранг'))
    bonus_for_line_1 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 1'), default=0)
    bonus_for_line_2 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 2'), default=0)
    bonus_for_line_3 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 3'), default=0)
    bonus_for_line_4 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 4'), default=0)
    bonus_for_line_5 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 5'), default=0)
    bonus_for_line_6 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 6'), default=0)
    bonus_for_line_7 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 7'), default=0)
    bonus_for_line_8 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 8'), default=0)
    bonus_for_line_9 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 9'), default=0)
    bonus_for_line_10 = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name=_('Бонус за линию 10'), default=0)

    class Meta:
        verbose_name = _('Многоуровневый бонус')
        verbose_name_plural = _('Многоуровневые бонусы')

    def __str__(self):
        return self.rang.title


class MultiLevelBonusHistory(models.Model):
    package_history = models.ForeignKey('packages.PackageHistory', on_delete=models.CASCADE, verbose_name=_('Запись в истории'))
    text = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Отчёт по многоуровневому бонусу')
        verbose_name_plural = _('Отчёты по многоуровневому бонусу')

    def __str__(self):
        return '{} > {}'.format(self.package_history.user.unique_number, self.package_history.package.title)


class PointAward(models.Model):
    rang = models.ForeignKey(RangAward, on_delete=models.CASCADE, verbose_name=_('Ранг'))
    bonus = models.DecimalField(verbose_name=_('Бонус'), max_digits=10, decimal_places=2)

    max_money = 10000

    class Meta:
        verbose_name = _('Схема конвертации баллов в FBC')
        verbose_name_plural = _('Схемы конвертации баллов в FBC')

    def __str__(self):
        return self.rang.title
