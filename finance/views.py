from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import UsersFinanceHistory


class FinanceHistoryListView(LoginRequiredMixin, ListView):
    template_name = 'finance/user-finance-history.html'
    context_object_name = 'finances'
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        return UsersFinanceHistory.objects.filter(user=self.request.user)
