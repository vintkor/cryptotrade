from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
    PosMaterialListView,
)


app_name = 'promo'
urlpatterns = [
    path('lessons/category/<int:pk>/', LessonListView.as_view(), name='lessons-list'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('pos-materials/', PosMaterialListView.as_view(), name='pos-materials'),
]
