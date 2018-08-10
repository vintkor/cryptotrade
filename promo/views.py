from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import (
    Lesson,
    PosMaterial,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LessonListView(LoginRequiredMixin, ListView):
    template_name = 'promo/lessons-list.html'
    context_object_name = 'lessons'
    login_url = reverse_lazy('user:login')
    
    def get_queryset(self):
        return Lesson.objects.filter(category__id=self.kwargs.get('pk'))


class LessonDetailView(LoginRequiredMixin, DetailView):
    template_name = 'promo/lesson-detail.html'
    context_object_name = 'lesson'
    model = Lesson
    login_url = reverse_lazy('user:login')


class PosMaterialListView(LoginRequiredMixin, ListView):
    template_name = 'promo/pos-materials.html'
    context_object_name = 'pos_materials'
    model = PosMaterial
    login_url = reverse_lazy('user:login')
