from django.db import models
from django.utils.translation import ugettext as _


class RangAward(models.Model):
    title = models.CharField(verbose_name=_('Заголовок'), max_length=60)
    volume = models.DecimalField(verbose_name=_('Объём'), max_digits=10, decimal_places=2)
    max_lines = models.PositiveSmallIntegerField(verbose_name=_('Количество линий'))
    lines_volume = models.DecimalField(verbose_name=_('Объём в линиях'), max_digits=10, decimal_places=2)
    include_rang = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('Ранг партнёров'), null=True, blank=True)
    include_rang_count = models.PositiveSmallIntegerField(verbose_name=_('Количество партнёров с указаным рангом'))
    bonus = models.DecimalField(verbose_name=_('Бонус'), max_digits=10, decimal_places=2)
    is_final = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Ранговый бонус')
        verbose_name_plural = _('Ранговые бонусы')
        ordering = ('-volume',)

    def __str__(self):
        return self.title
