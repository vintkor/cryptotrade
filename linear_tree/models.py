from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import User
from mptt.models import MPTTModel, TreeForeignKey


class LinearTree(MPTTModel):
    """
    Модель бинарного дерева
    """
    user = models.OneToOneField(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, verbose_name=_('Родитель'), db_index=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Линейное дерево')
        verbose_name_plural = _('Линейныу деревья')

    class MPTTMeta:
        order_insertion_by = ('user',)

    def __str__(self):
        return self.user.unique_number