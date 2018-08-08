from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from linear_tree.models import LinearTree
from binary_tree.models import BinaryTree
from news.models import News
from finance.models import UsersFinanceHistory


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get(self, request):
        context = {}

        l_parent = LinearTree.objects.get(user=self.request.user)
        l_queryset = LinearTree.objects.all()

        context['my_people'] = l_parent.get_children().count()
        context['my_stucture'] = l_parent.get_descendant_count()
        context['points'] = BinaryTree.objects.values('left_points', 'right_points').get(user=self.request.user)
        context['last_news'] = News.objects.all()[:10]
        context['last_finanses'] = UsersFinanceHistory.objects.filter(user=self.request.user)[:20]

        return render(request, 'dashboard/dashboard.html', context)
