from django.contrib import admin
from .models import (
    Package,
    PackageHistory,
)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'tokens',
        'bonuses',
        'points',
    )


@admin.register(PackageHistory)
class PackageHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'old_package',
        'package',
        'created',
        'uuid',
    )
