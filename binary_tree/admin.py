from django.contrib import admin
from .models import (
    BinaryTree,
    Reason,
    BinaryPointsHistory,
)
from mptt.admin import DraggableMPTTAdmin


@admin.register(BinaryTree)
class BinaryTreeAdmin(DraggableMPTTAdmin):
    save_on_top = True
    list_display = (
        'tree_actions',
        'indented_title',
        'left_node',
        'right_node',
        'left_points',
        'right_points',
        'created',
    )


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(BinaryPointsHistory)
class BinaryPointsHistoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'tree_node',
        'left_points',
        'right_points',
        'reason',
        'created',
    )