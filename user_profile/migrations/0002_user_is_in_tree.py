# Generated by Django 2.0.7 on 2018-07-12 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_in_tree',
            field=models.BooleanField(default=False, verbose_name='Участники бинарной структуры'),
        ),
    ]
