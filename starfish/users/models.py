from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
    )

    history = HistoricalRecords()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
