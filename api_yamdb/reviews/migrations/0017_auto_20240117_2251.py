# Generated by Django 3.2 on 2024-01-17 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Некорректный slug.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг категории'),
        ),
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Некорректный slug.', regex='^[-a-zA-Z0-9_]+$')], verbose_name='Слаг'),
        ),
    ]
