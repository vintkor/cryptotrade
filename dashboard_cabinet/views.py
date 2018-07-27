from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get(self, request):
        context = {}
        return render(request, 'cabinet.html', context)
