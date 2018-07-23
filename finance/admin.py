from django.contrib import admin
from .models import (
    Purpose,
    UsersFinanceHistory,
)


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
    )


@admin.register(UsersFinanceHistory)
class UsersFinanceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'purpose',
        'get_number',
        'get_number_second_user',
    )
    readonly_fields = ('uuid',)
