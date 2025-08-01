from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        (1, 'Admin'),
        (2, 'User'),
    )
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    role = models.IntegerField(choices=ROLES, default=2)

    def __str__(self):
        return self.username