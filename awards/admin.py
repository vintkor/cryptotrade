from django.contrib import admin
from .models import RangAward, MultiLevelBonus, MultiLevelBonusHistory, RangAwardHistory, PointAward


@admin.register(RangAward)
class RangAwardAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'volume',
        'max_lines',
        'lines_volume',
        'include_rang',
        'include_rang_count',
        'bonus',
        'is_final',
        'is_start',
        'quick_days',
        'quick_bonus',
    )


@admin.register(MultiLevelBonus)
class MultiLevelBonusAdmin(admin.ModelAdmin):
    list_display = (
        'rang',
        'bonus_for_line_1',
        'bonus_for_line_2',
        'bonus_for_line_3',
        'bonus_for_line_4',
        'bonus_for_line_5',
        'bonus_for_line_6',
        'bonus_for_line_7',
        'bonus_for_line_8',
        'bonus_for_line_9',
        'bonus_for_line_10',
    )


@admin.register(MultiLevelBonusHistory)
class MultiLevelBonusHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created',)


@admin.register(RangAwardHistory)
class RangAwardHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')


@admin.register(PointAward)
class PointAwardAdmin(admin.ModelAdmin):
    list_display = ('rang', 'bonus')
