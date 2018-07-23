from django.contrib import admin
from .models import RangAward


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
    )
