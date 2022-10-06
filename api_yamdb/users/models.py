import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        error_messages={
            'unique': ('Пользователь с таким именем существует.')
        },
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
        null=False
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default=uuid.uuid4,
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
