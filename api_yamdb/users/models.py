from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import UsernameValidator
from api_yamdb.settings import (AUTH_USERNAME_MAXLENGTH,
                                AUTH_EMAIL_MAXLENGTH,
                                AUTH_CONF_CODE_MAXLENGTH)


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор')
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=AUTH_USERNAME_MAXLENGTH,
        unique=True,
        help_text=(
            'Обязательное поле. 150 символов или меньше'
            'Латинские буквы, цифры и @/./+/-/_ .'
        ),
        validators=(UsernameValidator(),),
        error_messages={'unique': "Такой пользователь уже зарегистрирован."}
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=AUTH_EMAIL_MAXLENGTH,
        unique=True,
        error_messages={'unique': "Такой адрес уже зарегистрирован."}
    )
    bio = models.TextField(
        'О себе',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Ролевая группа',
        max_length=max(len(role[0]) for role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=AUTH_CONF_CODE_MAXLENGTH,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('-id',)

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ROLE_ADMIN
            or self.is_superuser
            or self.is_staff
        )

    def __str__(self):
        return self.username
