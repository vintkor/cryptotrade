from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _
from .managers import UserManager
from geo.models import Country


STATUS_CHOICES = (
    ('1', 'Неактивный'),
    ('2', 'Активный'),
    ('3', 'Заморожен'),
    ('4', 'Полное заполнение'),
)


DIRECTION_CHOICES = (
    ('left', _('Влево')),
    ('right', _('Вправо')),
)

def get_status_text(key):
    for i in STATUS_CHOICES:
        if i[0] == str(key):
            return i[1]
    return False


class User(AbstractBaseUser, PermissionsMixin):
    """
    Пользователи системы
    """
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name=_('Спонсор'), null=True, blank=True)
    email = models.EmailField(verbose_name=_('email'), max_length=255, unique=True, db_index=True)
    avatar = models.ImageField(verbose_name=_('Аватар'), blank=True, null=True, upload_to="user/avatar")
    first_name = models.CharField(verbose_name=_('Фамилия'), max_length=40)
    last_name = models.CharField(verbose_name=_('Имя'), max_length=40)
    login = models.CharField(max_length=30, verbose_name=_('Логин'), unique=True)
    phone = models.CharField(max_length=30, unique=True, verbose_name=_('Номер телефона'), null=True, blank=True)
    unique_number = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name=_('Уникальный номер'))
    date_of_birth = models.DateField(_('Дата рождения'), null=True, blank=True)
    is_in_tree = models.BooleanField(default=False, verbose_name=_('Участники бинарной структуры'))
    is_active = models.BooleanField(_('Активен'), default=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=_('Статус'), default='1')
    ref_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('Страна'), null=True)
    registration_direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES,
                                    default=DIRECTION_CHOICES[0][0], verbose_name=_('Направление регистрации'))
    is_admin = models.BooleanField(_('Суперпользователь'), default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))
    is_verified = models.BooleanField(verbose_name=_('Верифицирован'), default=False)
    balance = models.DecimalField(verbose_name=_('Баланс'), decimal_places=2, max_digits=10, default=0)
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, verbose_name=_('Пакет'), blank=True, null=True)
    rang = models.ForeignKey('awards.RangAward', on_delete=models.CASCADE, verbose_name=_('Ранг'), blank=True, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-unique_number']

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        elif self.first_name:
            return '{} {}'.format(self.first_name, self.email)
        elif self.last_name:
            return '{} {}'.format(self.last_name, self.email)
        else:
            return self.email

    def save(self, *args, **kwargs):
        if self.unique_number is None:
            last_user = User.objects.first()
            if last_user is None:
                new_code = 'CT-1000000'
            else:
                last_code = last_user.unique_number.split('-')
                new_code = '{}-{}'.format(last_code[0], (int(last_code[1]) + 1))
            self.unique_number = new_code

        if self.ref_code is None:
            is_true = True
            while is_true:
                ref_code = get_random_string(10, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHZKWX1234567890')
                if not User.objects.filter(ref_code=ref_code).exists():
                    self.ref_code = ref_code
                    is_true = False

        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def set_status_not_active(self):
        self.status = '1'

    def set_status_active(self):
        self.status = '2'

    def set_status_frozen(self):
        self.status = '3'

    # def get_rang(self):
    #     if self.rang:
    #         return True, self.rang
    #     return False, 'No Rank'
