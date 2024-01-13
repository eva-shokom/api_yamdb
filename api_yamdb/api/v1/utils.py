from django.conf import settings
from django.contrib.auth.tokens import default_token_generator


def send_confirmation_email(user, confirmation_code):
    subject = f'Код подтверждения для {user.username}'
    message = f'Ваш код подтверждения {confirmation_code}'
    from_email = settings.ADMIN_EMAIL
    user.email_user(subject, message, from_email)


def check_confirmation_code(user, confirmation_code):
    return default_token_generator.check_token(user, confirmation_code)
