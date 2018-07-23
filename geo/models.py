from django.db import models
from django.utils.translation import ugettext as _


class Country(models.Model):
    title = models.CharField(max_length=150, verbose_name=_('Заголовок'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Страна')
        verbose_name_plural = _('Страны')

    def __str__(self):
        return self.title
