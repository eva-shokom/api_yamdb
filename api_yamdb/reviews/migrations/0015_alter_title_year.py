# Generated by Django 3.2 on 2024-01-15 20:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20240113_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MaxValueValidator(2024, message='Год не может быть больше текущего!')], verbose_name='Год'),
        ),
    ]
