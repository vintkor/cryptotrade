from django.contrib import admin
from user_profile.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'unique_number',
        'email',
        'first_name',
        'last_name',
        'phone',
        'country',
        'is_in_tree',
        'status',
        'package',
        'rang',
        'is_verified',
        'balance',
        'volume',
        'is_admin',
    )
    readonly_fields = (
        'created',
        'password',
        'unique_number',
        'ref_code',
    )
    list_filter = (
        'is_admin',
        'is_verified',
        'package',
        'rang',
    )
    list_editable = ('rang', 'package', 'volume')
    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
