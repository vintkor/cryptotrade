# Generated by Django 2.0.7 on 2018-07-20 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0003_auto_20180720_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='rangaward',
            name='is_final',
            field=models.BooleanField(default=False),
        ),
    ]
