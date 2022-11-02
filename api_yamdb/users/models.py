from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор')
    ]
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=128,
        unique=True
    )
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        'Ролевая группа',
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        return self.username
