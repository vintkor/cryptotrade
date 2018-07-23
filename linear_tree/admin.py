from django.contrib import admin
from .models import LinearTree
from mptt.admin import DraggableMPTTAdmin


@admin.register(LinearTree)
class LinearTreeAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'user',
        'created',
    )

