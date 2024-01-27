from django.contrib.auth.models import AbstractUser
from django.db import models


class Auth(AbstractUser):
    username = None

    phone = models.CharField(unique=True, max_length=35, verbose_name='номер телефона')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
