from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from api_yamdb.settings import EMAIL_CONFIRMATION
from .models import User


def create_and_send_code(username):
    user = get_object_or_404(User, username=username)
    code = get_random_string(length=5)
    user.confirmation_code = code
    user.save()
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения для получения токена: {code}.',
        EMAIL_CONFIRMATION,
        [f'{user.email}'],
        fail_silently=False,
    )
