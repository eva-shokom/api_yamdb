import re

from django.core.exceptions import ValidationError


def username_not_me(value):
    if re.match(r'^me$', value, re.IGNORECASE):
        raise ValidationError(f'Имя пользователя {value} запрещено.')
