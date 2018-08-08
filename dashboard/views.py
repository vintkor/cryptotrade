from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View
from linear_tree.models import LinearTree
from binary_tree.models import BinaryTree


class DashboardView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get(self, request):
        context = {}

        l_parent = LinearTree.objects.get(user=self.request.user)
        l_queryset = LinearTree.objects.all()

        my_people = l_parent.get_children().count()
        my_stucture = l_parent.get_descendant_count()

        points = BinaryTree.objects.values('left_points', 'right_points').get(user=self.request.user)
        print(points)

        context['my_people'] = my_people
        context['my_stucture'] = my_stucture
        context['points'] = points

        return render(request, 'dashboard/dashboard.html', context)
