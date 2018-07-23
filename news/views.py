from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import News


class NewsListView(LoginRequiredMixin, ListView):
    template_name = 'news/news-list.html'
    context_object_name = 'newses'
    model = News
    login_url = reverse_lazy('user:login')


class NewsDetailView(DetailView):
    template_name = 'news/news-detail.html'
    context_object_name = 'news'
    model = News
    login_url = reverse_lazy('user:login')
