# Generated by Django 3.2 on 2024-01-11 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_title_year'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_media',
        ),
    ]
