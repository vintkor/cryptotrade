from django.db import models
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse
from .validators import youtube_validator


class LessonCategory(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Название'))
    sort = models.PositiveSmallIntegerField(verbose_name=_('Sorted'), default=0)

    class Meta:
        verbose_name = _('Категория уроков')
        verbose_name_plural = _('Категории уроков')
        ordering = ('sort',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('promo:lessons-list', kwargs={'pk': self.id})


class Lesson(models.Model):
    category = models.ForeignKey(LessonCategory, on_delete=models.CASCADE, verbose_name=_('Категория'))
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='promo/video-lessons/', blank=True, null=True)
    video = models.URLField(verbose_name='YouTube Видео', validators=[youtube_validator], blank=True, null=True)
    description = RichTextUploadingField(verbose_name=_('Описание урока'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))
    sort = models.PositiveSmallIntegerField(verbose_name=_('Sorted'), default=0)

    class Meta:
        verbose_name = _('Урок')
        verbose_name_plural = _('Уроки')
        ordering = ('sort',)

    def __str__(self):
        return self.title

    def is_video(self):
        if self.video:
            return True
        return False

    def get_absolute_url(self):
        return reverse('promo:lesson-detail', kwargs={'pk': self.id})


class PosMaterial(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='promo/POS/')

    class Meta:
        verbose_name = _('POS материал')
        verbose_name_plural = _('POS материалы')

    def __str__(self):
        return self.title
