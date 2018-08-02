from django.contrib import admin
from .models import (
    Purpose,
    UsersFinanceHistory,
    PaymentSystem,
    PaymentHistory,
)
from django.contrib.postgres.fields import JSONField
from jsoneditor.forms import JSONEditor


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


@admin.register(PaymentSystem)
class PaymentSystemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'payment_system',
        'amount',
        'is_success',
        'created',
    )
