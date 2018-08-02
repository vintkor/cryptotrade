from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import LinearTree
from django.contrib.auth.mixins import LoginRequiredMixin


class LinearTreeListView(LoginRequiredMixin, ListView):
    model = LinearTree
    context_object_name = 'nodes'
    template_name = 'linear_tree/linear_tree.html'
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        node = LinearTree.objects.get(user_id=self.request.user.id)

        linear = LinearTree.get_descendants(node, include_self=True).values(
            'parent',
            'user__avatar',
            'user__first_name',
            'user__last_name',
            'user__unique_number',
            'user_id',
            'user__parent',
            'id',
            'user__rang__title',
            'user__package__title',
        )
        return linear
