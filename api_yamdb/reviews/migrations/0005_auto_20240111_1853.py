# Generated by Django 3.2 on 2024-01-11 13:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_title_unique_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(0, message='Год не может быть отрицательным!'), django.core.validators.MaxValueValidator(2024, message='Год не может быть больше текущего!')], verbose_name='Год'),
        ),
    ]