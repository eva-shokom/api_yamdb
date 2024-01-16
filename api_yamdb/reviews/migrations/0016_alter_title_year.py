# Generated by Django 3.2 on 2024-01-15 20:29

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[reviews.validators.validate_year], verbose_name='Год'),
        ),
    ]
