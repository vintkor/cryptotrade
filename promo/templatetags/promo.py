from django import template
from promo.models import LessonCategory

register = template.Library()


@register.simple_tag
def get_lesson_categories():
    return LessonCategory.objects.all()
