from django.urls import path
from .views import (
    LessonListView,
    LessonDetailView,
)


app_name = 'promo'
urlpatterns = [
    path('lessons/category/<int:pk>/', LessonListView.as_view(), name='lessons-list'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
