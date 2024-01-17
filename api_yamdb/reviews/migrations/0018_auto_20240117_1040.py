# Generated by Django 3.2 on 2024-01-17 07:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_merge_20240117_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Имя категории'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(0, message='Год не может быть отрицательным!'), django.core.validators.MaxValueValidator(2024, message='Год не может быть больше текущего!')], verbose_name='Год'),
        ),
    ]