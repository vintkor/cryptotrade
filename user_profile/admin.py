from django.contrib import admin
from user_profile.models import User, Document, TopUsers


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (DocumentInline,)
    list_display = (
        'unique_number',
        'email',
        'first_name',
        'last_name',
        'balance',
        'phone',
        'country',
        'is_in_tree',
        'status',
        'package',
        'rang',
        'verification',
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
        'verification',
        'package',
        'rang',
    )
    list_editable = ('rang', 'package', 'volume')
    search_fields = ('email', 'unique_number',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(TopUsers)
class TopUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
