# Generated by Django 2.0.7 on 2018-07-30 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0004_rangaward_is_final'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiLevelBonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus_for_line_1', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 1')),
                ('bonus_for_line_2', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 2')),
                ('bonus_for_line_3', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 3')),
                ('bonus_for_line_4', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 4')),
                ('bonus_for_line_5', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 5')),
                ('bonus_for_line_6', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 6')),
                ('bonus_for_line_7', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 7')),
                ('bonus_for_line_8', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 8')),
                ('bonus_for_line_9', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 9')),
                ('bonus_for_line_10', models.DecimalField(decimal_places=1, default=0, max_digits=3, verbose_name='Бонус за линию 10')),
                ('rang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='awards.RangAward', verbose_name='Ранг')),
            ],
            options={
                'verbose_name': 'Многоуровневый бонус',
                'verbose_name_plural': 'Многоуровневые бонусы',
            },
        ),
    ]
