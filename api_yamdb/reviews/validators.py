from django.core.validators import MaxValueValidator
from django.utils import timezone


def validate_year():
    MaxValueValidator(
        timezone.now().year,
        message='Значение года больше текущего!'
    )
