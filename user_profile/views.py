from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import (
    User,
    Document,
)
from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
    View,
    ListView,
)
from .forms import (
    RegistrationByRefCodeForm,
    AuthForm,
    VerificationForm,
    AuthChangePasswordForm)
from django.db.transaction import atomic
from binary_tree.models import BinaryTree
from linear_tree.models import LinearTree
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.crypto import get_random_string
from PIL import Image
import os
from cryptotrade.settings import MEDIA_ROOT, MEDIA_URL
from django.contrib.auth.models import Permission
from cryptotrade.settings import DONT_HAVE_PERMISSION, ADMIN_EMAIL
from .tasks import (
    send_simple_email_task,
    send_simple_sms_task,
)


class NewUserByRefCodeView(FormView):
    form_class = RegistrationByRefCodeForm
    template_name = 'user_profile/register-by-ref-code.html'

    def get_form_kwargs(self):
        kwargs = super(NewUserByRefCodeView, self).get_form_kwargs()
        parent = get_object_or_404(User, ref_code=self.kwargs.get('ref_code'))
        kwargs['parent'] = parent
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        return super(NewUserByRefCodeView, self).dispatch(request, *args, **kwargs)

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


class VerificationFormView(LoginRequiredMixin, UpdateView):
    context_object_name = 'user'
    template_name = 'user_profile/verification.html'
    login_url = reverse_lazy('user:login')
    form_class = VerificationForm

    def get_context_data(self, **kwargs):
        context = super(VerificationFormView, self).get_context_data(**kwargs)
        context['documents'] = Document.objects.filter(user=self.request.user)
        return context

    def get_object(self):
        user = User.objects.select_related('country').get(pk=self.request.user.id)
        return user

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action')
        if action == 'need_codes':
            email_code = get_random_string(length=5, allowed_chars='0123456789')
            phone_code = get_random_string(length=5, allowed_chars='0123456789')

            self.request.session['email_code'] = email_code
            self.request.session['phone_code'] = phone_code

            email_users = self.get_object().email
            email_subject = _('Код верификации email CryptoTrade')
            email_text = _('Ваш код - {}'.format(email_code))

            send_simple_email_task.delay(email_users, email_subject, email_text)

            phone = self.get_object().phone
            message = _('Ваш код подтверждения: {}'.format(phone_code))
            send_simple_sms_task.delay(phone, message)

            return JsonResponse({
                'status': True,
            })

        if action == 'check_codes':

            email_code = self.request.session.get('email_code')
            phone_code = self.request.session.get('phone_code')

            user_email_code = self.request.POST.get('email_code')
            user_phone_code = self.request.POST.get('phone_code')

            if email_code == user_email_code and phone_code == user_phone_code:
                user = self.get_object()
                user.set_verification_need_check()
                user.is_valid_email = True
                user.is_valid_phone = True
                user.save(update_fields=('verification', 'is_valid_email', 'is_valid_phone',))

                email_users = ADMIN_EMAIL
                email_subject = 'Запрос на верификацию'
                email_text = """
                    Поступил новый запрос на верификацию от пользователя {user}
                """.format(user=user.unique_number)
                send_simple_email_task.delay(email_users, email_subject, email_text)

                return JsonResponse({
                    'status': True,
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': _('Коды веривикации не верные')
                })

        if action == 'check_documents':
            user = self.get_object()
            user.set_verification_need_check()
            user.save(update_fields=('verification',))

            email_users = ADMIN_EMAIL
            email_subject = 'Запрос на верификацию'
            email_text = """
                                Поступил новый запрос на верификацию от пользователя {user}
                            """.format(user=user.unique_number)
            send_simple_email_task.delay(email_users, email_subject, email_text)

            return JsonResponse({
                'status': True,
            })

        user = self.get_object()
        user.set_verification_need_email_and_sms()
        user.save(update_fields=('verification',))
        return super(VerificationFormView, self).post(request, *args, **kwargs)


class VerificationDocumentLoaderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('user:login')

    def post(self, request):
        path = MEDIA_ROOT + '/verification'
        if not os.path.isdir(path):
            os.makedirs(path)

        file = request.FILES.get('file')
        ext = file.name.split('.')[-1]
        file_name = 'verification/{}__{}.{}'.format(request.user.id, get_random_string(length=20), ext)

        image = Image.open(file)
        image.save(MEDIA_ROOT + '/' + file_name)

        document = Document(
            user=self.request.user,
            image=file_name,
        )
        document.save()
        return HttpResponse()


class VerificationsListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'user_profile/verification-users.html'
    context_object_name = 'users'
    queryset = User.objects.filter(verification='5')
    permission_required = ['user_profile.can_verify']
    login_url = reverse_lazy('user:login')

    def handle_no_permission(self):
        messages.error(self.request, _(DONT_HAVE_PERMISSION), 'danger')
        return super(VerificationsListView, self).handle_no_permission()


class VerificationUserDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = 'user_profile/verification-user-detail.html'
    context_object_name = 'v_user'
    model = User
    permission_required = ['user_profile.can_verify']
    login_url = reverse_lazy('user:login')

    def handle_no_permission(self):
        messages.error(self.request, _(DONT_HAVE_PERMISSION), 'danger')
        return super(VerificationUserDetailView, self).handle_no_permission()

    def post(self, request, pk):
        action = self.request.POST.get('action')
        actions = ['verify_user', 'refuse', 'recheck', 'need_documents']
        user = self.get_object()

        if action not in actions:
            return JsonResponse({
                'status': False,
                'message': _('Неверный запрос')
            })

        # verify
        if action == actions[0]:
            permission = Permission.objects.get(name='is_verified')
            user.user_permissions.add(permission)
            user.set_verification_verify()
            user.save(update_fields=('verification',))
            send_simple_email_task.delay(
                user.email,
                _('Верификация CryptoTrade'),
                _('Вы успешно верифицированы. Теперь вам открыт полный дуступ к системе'),
            )
            return JsonResponse({
                'status': True
            })

        # refuse
        if action == actions[1]:
            user.set_verification_refuse()
            user.save(update_fields=('verification',))

            send_simple_email_task.delay(
                user.email,
                _('Верификация CryptoTrade'),
                _('Вам было отказано в верификации'),
            )

            return JsonResponse({
                'status': True,
                'redirect_url': reverse_lazy('user:verification-users')
            })

        # recheck
        if action == actions[2]:
            pass

        # Need some documents
        if action == actions[3]:
            message = self.request.POST.get('message')
            user.set_verification_need_documents()
            user.save(update_fields=('verification',))

            send_simple_email_task.delay(
                user.email,
                _('Верификация CryptoTrade'),
                _('Вам необходимо добавить следующие документы: {}'.format(message)),
            )

            return JsonResponse({
                'status': True,
                'redirect_url': reverse_lazy('user:verification-users')
            })

        return JsonResponse({
            'status': False,
            'message': _('Неверный формат запроса')
        })


class ChangeDirectionView(View):

    def post(self, request):
        direction = self.request.POST.get('action')

        if direction and direction in ['left', 'right']:
            self.request.user.registration_direction = direction
            self.request.user.save(update_fields=('registration_direction',))

            return JsonResponse({
                'status': True,
            })

        return JsonResponse({
            'status': False,
        })


class UserChangePasswordView(FormView):
    template_name = 'user_profile/change-password.html'
    form_class = AuthChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super(UserChangePasswordView, self).get_form_kwargs()
        user = self.request.user
        if user:
            kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        new_pass = form.cleaned_data.get('new_password')

        user.set_password(new_pass)
        user.save()

        send_simple_email_task.delay(
            user.email,
            _('CryptoTrade - смена пароля'),
            'Ваш пароль успешно изменён на >> {} <<. Сохраните этот пароль и удалите пожалуйста это письмо.'.format(
                new_pass
            ),
        )

        return redirect(reverse_lazy('user:profile'))


class ChangoProfilePhotoView(View):

    def get(self, request):
        context = {}
        return render(request, 'user_profile/change-profile-photo.html', context)

    def post(self, request):

        if request.POST.get('imageWidth', False):
            image_width = int(float(request.POST.get('imageWidth')))
            image_height = int(float(request.POST.get('imageHeight')))
            image_x = int(float(request.POST.get('image_x')))
            image_y = int(float(request.POST.get('image_y')))
            image_file = request.FILES.get('image')
            rotate_deg = request.POST.get('rotate')

            ext = image_file.name.split('.')[-1]

            image = Image.open(image_file)
            rotate_image = image.rotate(int(rotate_deg))
            cropped_image = rotate_image.crop((image_x, image_y, image_width + image_x, image_height + image_y))
            resized_image = cropped_image.resize((image_width, image_height), Image.ANTIALIAS)

            file_name = 'user/avatar/profile__{}__{}.{}'.format(request.user.pk, get_random_string(length=10), ext)

            resized_image.save('{}/{}'.format(MEDIA_ROOT, file_name))

            request.user.avatar = file_name
            request.user.save(update_fields=('avatar',))

            return JsonResponse({
                'status': 1,
                'image_url': MEDIA_URL + file_name
            })

        return JsonResponse({
            'status': 0,
        })
