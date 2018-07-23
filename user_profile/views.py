from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import (
    User,
)
from django.views.generic import (
    FormView,
    DetailView)
from .forms import (
    RegistrationByRefCodeForm,
    AuthForm,
)
from django.db.transaction import atomic
from binary_tree.models import BinaryTree
from linear_tree.models import LinearTree
from django.contrib import messages
from django.utils.translation import ugettext as _


class NewUserByRefCodeView(FormView):
    form_class = RegistrationByRefCodeForm
    template_name = 'user_profile/register-by-ref-code.html'

    def get_form_kwargs(self):
        kwargs = super(NewUserByRefCodeView, self).get_form_kwargs()
        parent = get_object_or_404(User, ref_code=self.kwargs.get('ref_code'))
        kwargs['parent'] = parent
        return kwargs

    def form_valid(self, form):
        parent = User.objects.get(ref_code=form.cleaned_data['parent'])
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        with atomic():
            new_user = User()
            new_user.login = form.cleaned_data['login']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = email
            new_user.set_password(password)
            new_user.parent = parent
            new_user.phone = form.cleaned_data['phone']
            new_user.is_in_tree = True
            new_user.country_id = form.cleaned_data['country'].id
            new_user.save()

            parent_in_b_tree = BinaryTree.objects.get(user=parent)
            new_b_user = parent_in_b_tree.set_user_to_tree(parent.registration_direction, new_user.pk)

            setattr(new_b_user.parent, parent.registration_direction + '_node', new_b_user.id)
            new_b_user.parent.save(update_fields=('left_node', 'right_node'))

            parent_in_l_tree = LinearTree.objects.get(user=parent)
            new_l_user = LinearTree(
                parent=parent_in_l_tree,
                user=new_user,
            )
            new_l_user.save()

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('dashboard:dashboard')


class AuthView(FormView):
    form_class = AuthForm
    template_name = 'user_profile/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')

        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('dashboard:dashboard')

        messages.error(self.request, _('Не верный адрес почты или пароль'), 'danger')
        return redirect(self.request.META.get('HTTP_REFERER'))


def user_logout(request):
    logout(request)
    return redirect('user:login')


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'user'
    template_name = 'user_profile/user-profile.html'
    login_url = reverse_lazy('user:login')

    def get_object(self):
        user = User.objects.select_related('country').get(pk=self.request.user.id)
        return user

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['ref_link'] = reverse_lazy('user:register-by-ref', kwargs={'ref_code': self.get_object().ref_code})
        return context
