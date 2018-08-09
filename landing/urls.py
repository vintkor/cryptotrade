from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import LandingRefView, LandingView

app_name = 'landing'
urlpatterns = [
    path('', LandingView.as_view(), name='home'),
    path('r/<str:ref_code>/', LandingRefView.as_view(), name='home-ref'),
]
