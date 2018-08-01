from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import BinaryTree, BinaryPointsHistory
from django.views.generic import View, ListView
import json


def get_parameters(request):
    try:
        parameters = json.loads(request.decode('utf-8'))
    except:
        return False

    return parameters


def bad_request():
    context = {
        'status': False,
        'message': 'Не верный формат запроса',
    }
    return JsonResponse(context)


class BinaryTreeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def get(self, request):
        context = {}
        return render(request, 'binary_tree/binary_tree.html', context)

    def post(self, request):
        context = {}
        tree_deep = 13

        parameters = get_parameters(self.request.body)
        if not parameters:
            return bad_request()

        username = parameters.get('root_node')
        if username:
            try:
                node = BinaryTree.objects.get(user__unique_number=username)
            except BinaryTree.DoesNotExist:
                context['status'] = False
                context['message'] = 'Пользователя {} не существует'.format(username)
                return JsonResponse(context)
        else:
            return bad_request()

        tree = list()
        nodes = node.get_descendants(include_self=True).filter(level__lte=tree_deep)

        for ind, i in enumerate(nodes):
            element = dict()
            element['id'] = i.id
            element['name'] = i.user.unique_number
            element['parentId'] = i.parent.id if i.parent else None

            if ind == 0:
                element['parentId'] = None

            if i.user.unique_number == self.request.user.unique_number:
                element['parentId'] = None

            element['level'] = i.level
            element['left_node'] = i.left_node if i.left_node else False
            element['right_node'] = i.right_node if i.right_node else False
            element['left_points'] = 'Left - {}'.format(i.left_points)
            element['right_points'] = 'Right - {}'.format(i.right_points)
            element['status'] = i.user.status
            element['created'] = i.created
            element['image'] = i.user.avatar.url if i.user.avatar else None
            element['full_name'] = i.user.get_full_name()
            icon_template = "<span class='package_weight'><i class='fa fa-3x fa-{} {}-{}'></i></span>"
            element['package_weight'] = icon_template.format('battery', 'package', i.user.package.title) if i.user.package else "<span class='hidden'>1</span>"
            element['rang'] = icon_template.format('circle', 'rang', i.user.rang.title) if i.user.rang else "<span class='hidden'>1</span>"

            if node.left_node or node.right_node:
                element[
                    'look_tree'] = "<a class='look_tree' href='{}'><i class='fa fa-3x fa-chevron-down'></i></a>".format(
                    i.user.unique_number)
            else:
                element['look_tree'] = "<span class='hidden'>1</span>"

            if i.level == tree_deep:
                element['skip_children'] = True

            tree.append(element)

        context['status'] = True
        context['tree'] = tree

        return JsonResponse(context)


class PointsHistoryListView(LoginRequiredMixin, ListView):
    context_object_name = 'histories'
    template_name = 'binary_tree/points-history.html'
    login_url = reverse_lazy('user:login')

    def get_queryset(self):
        histories = BinaryPointsHistory.objects.filter(tree_node__user=self.request.user)
        return histories

    # TODO Добавить пагинацию
