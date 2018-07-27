from django.urls import path, include
from .views import DashboardView

app_name = 'dashboard_cabinet'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]
