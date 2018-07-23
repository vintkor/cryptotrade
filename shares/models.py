from django.db import models
from user_profile.models import User
from django.utils.translation import ugettext as _


class Course(models.Model):
    course = models.DecimalField(verbose_name=_('Курс'), max_digits=8, decimal_places=5)

    class Meta:
        verbose_name = _('Курс токена')
        verbose_name_plural = _('Курсы токена')

    def __str__(self):
        return str(self.course)

    @staticmethod
    def get_last_course():
        return Course.objects.last()


class ShareHolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользоваиель'))
    amount = models.PositiveIntegerField(verbose_name=_('Количество'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('Курс'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Держатель токенов')
        verbose_name_plural = _('Держатели токенов')

    def __str__(self):
        return self.amount
