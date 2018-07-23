# Generated by Django 2.0.7 on 2018-07-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20180716_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='registration_direction',
            field=models.CharField(choices=[('left', 'Влево'), ('right', 'Вправо')], default='left', max_length=10, verbose_name='Направление регистрации'),
        ),
    ]
