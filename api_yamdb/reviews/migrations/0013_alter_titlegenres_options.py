# Generated by Django 3.2 on 2024-01-11 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_alter_title_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='titlegenres',
            options={'ordering': ('genre',), 'verbose_name': 'Произведение-Жанр', 'verbose_name_plural': 'Произведения-Жанры'},
        ),
    ]
