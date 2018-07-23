from django.urls import path
from .views import (
    FinanceHistoryListView,
)


app_name = 'finance'
urlpatterns = [
    path('history/', FinanceHistoryListView.as_view(), name='finance-history'),
]
