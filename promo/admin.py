from django.contrib import admin
from .models import (
    LessonCategory,
    Lesson,
    PosMaterial,
)


@admin.register(LessonCategory)
class LessonCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
    )
    list_filter = ('category',)


@admin.register(PosMaterial)
class PosMaterialAdmin(admin.ModelAdmin):
    pass
