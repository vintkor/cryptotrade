from django.contrib import admin
from .models import Course, ShareHolder


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(ShareHolder)
class ShareHolderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'course',
        'created',
    )
