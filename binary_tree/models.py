from django.db import models
from django.utils.translation import ugettext as _
from user_profile.models import User
from mptt.models import MPTTModel, TreeForeignKey


def find_node_to_append(nodes, direction, node_id):
    info = None
    for node in nodes:
        if node['id'] == node_id:
            if not node[direction]:
                node['leg_to_save'] = direction
                info = node
                break
            else:
                return find_node_to_append(nodes, direction, node[direction])
    return info


class BinaryTree(MPTTModel):
    """
    Модель бинарного дерева
    """
    user = models.ForeignKey(User, verbose_name=_('Пользователь'), on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True, verbose_name=_('Родитель'), db_index=True, on_delete=models.SET_NULL)
    left_node = models.PositiveIntegerField(verbose_name=_('Левый ребёнок'), default=None, blank=True, null=True)
    right_node = models.PositiveIntegerField(verbose_name=_('Правый ребёнок'), default=None, blank=True, null=True)
    left_points = models.PositiveIntegerField(verbose_name=_('Баллы в левой ноге'), default=0, blank=True, null=True)
    right_points = models.PositiveIntegerField(verbose_name=_('Баллы в правой ноге'), default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = _('Бинарное дерево')
        verbose_name_plural = _('Бинарные деревья')

    class MPTTMeta:
        order_insertion_by = ('user',)

    def __str__(self):
        return self.user.unique_number

    def _build_list(self):
        """ Строим список словарей дерева пользователя """
        nodes_list = []
        p = self.get_descendants(include_self=True).values(
            'id',
            'user__unique_number',
            'user__parent_id',
            'user__registration_direction',
            'left_node',
            'right_node',
        )
        for item in p:
            nodes_list.append(dict(
                id=item['id'],
                username=item['user__unique_number'],
                parent=item['user__parent_id'],
                direction=item['user__registration_direction'],
                left_node=item['left_node'],
                right_node=item['right_node'],
            ))
        return nodes_list

    def set_user_to_tree(self, direction, new_user_id):
        if direction not in ('left', 'right'):
            raise ValueError('Direction must be left or right')

        nodes = self._build_list()
        node_to_append = find_node_to_append(nodes, direction + '_node', self.id)

        new_node = BinaryTree()
        new_node.user_id = new_user_id
        new_node.parent_id = node_to_append['id']
        new_node.save()
        return new_node


class Reason(models.Model):
    """
    Основание для начисления или списания баллов
    Константы:
        1101 - Начисление баллов при регистрации/апгрейде пользователя в бинарном дереве
        1102 - Списание баллов на основании премии
    """
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    description = models.TextField(verbose_name=_('Описание'))
    code = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        verbose_name = _('Основание для начисления или списания баллов')
        verbose_name_plural = _('Основания для начисления или списания баллов')

    def __str__(self):
        return self.title


class BinaryPointsHistory(models.Model):
    """
    История начисления и списания баллов
    """
    tree_node = models.ForeignKey(BinaryTree, verbose_name=_('Пользователь'), on_delete=models.SET_NULL, blank=True, null=True)
    left_points = models.IntegerField(verbose_name=_('Баллы с лева'), blank=True, null=True)
    right_points = models.IntegerField(verbose_name=_('Баллы с права'), blank=True, null=True)
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Основание'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name = 'История начисления и списания баллов'
        verbose_name_plural = 'История начисления и списания баллов'

    def __str__(self):
        return self.tree_node.user
