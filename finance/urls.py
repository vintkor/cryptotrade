from django.urls import path
from .views import (
    FinanceHistoryListView,
    SendMoneyFormView,
)


app_name = 'finance'
urlpatterns = [
    path('history/', FinanceHistoryListView.as_view(), name='finance-history'),
    path('send-money/', SendMoneyFormView.as_view(), name='send-money'),
]
