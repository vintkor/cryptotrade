from django.db import models
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField
from django.shortcuts import reverse


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('Заголовок'))
    is_for_only_partners = models.BooleanField(default=False, verbose_name=_('Только для партнёров?'))
    image = models.ImageField(verbose_name=_('Изображение'), upload_to='media/news/', blank=True, null=True)
    text = RichTextUploadingField(verbose_name=_('Текст'))
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Дата создания'))

    class Meta:
        verbose_name_plural = _('Новости')
        verbose_name = _('Новость')
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.id})
