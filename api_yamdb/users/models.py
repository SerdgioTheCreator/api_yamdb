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
    bio = models.TextField(
        'О себе',
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )
    confirmation_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR
    
    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN