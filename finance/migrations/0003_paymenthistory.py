# Generated by Django 2.0.7 on 2018-07-31 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finance', '0002_paymentsystem'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('is_success', models.BooleanField(default=False, verbose_name='Является успешной')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('payment_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.PaymentSystem', verbose_name='Платёжная система')),
                ('user', models.ForeignKey(max_length=20, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'История платежей',
                'verbose_name_plural': 'Истории платежей',
            },
        ),
    ]
