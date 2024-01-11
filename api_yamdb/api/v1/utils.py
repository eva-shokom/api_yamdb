from django.conf import settings


def send_confirmation_email(user, confirmation_code):
    subject = f'Код подтверждения для {user.username}'
    message = f'Ваш код подтверждения {confirmation_code}'
    from_email = settings.ADMIN_EMAIL
    user.email_user(subject, message, from_email)
