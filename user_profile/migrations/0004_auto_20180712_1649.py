# Generated by Django 2.0.7 on 2018-07-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='unique_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Уникальный номер'),
        ),
    ]
