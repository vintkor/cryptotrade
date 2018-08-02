from django.urls import path
from .views import (
    FinanceHistoryListView,
    SendMoneyFormView,
    AddMoneyBaseView,
    PayeerFailView,
    PayeerStatusView,
)


app_name = 'finance'
urlpatterns = [
    path('history/', FinanceHistoryListView.as_view(), name='finance-history'),
    path('send-money/', SendMoneyFormView.as_view(), name='send-money'),
    path('add-money/', AddMoneyBaseView.as_view(), name='add-money'),
    path('payments/payeer/success/', AddMoneyBaseView.as_view(), name='payeer-success'),
    path('payments/payeer/fail/', PayeerFailView.as_view(), name='payeer-fail'),
    path('payments/payeer/status/', PayeerStatusView.as_view(), name='payeer-status'),
]
