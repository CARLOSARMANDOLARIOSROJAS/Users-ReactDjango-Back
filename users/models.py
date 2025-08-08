from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomUnicodeUsernameValidator(UnicodeUsernameValidator):
    """Validador personalizado que permite espacios en el username"""
    regex = r'^[a-zA-Z0-9_.@+\-\s]+$'
    message = 'Ingrese un nombre de usuario válido. Este valor puede contener solo letras, números, espacios y los caracteres @/./+/-/_.'

class User(AbstractUser):
    ROLES = (
        (1, 'Admin'),
        (2, 'User'),
    )
    
    # Sobrescribir el campo username para permitir espacios
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Requerido. 150 caracteres o menos. Letras, números, espacios y @/./+/-/_ únicamente.',
        validators=[CustomUnicodeUsernameValidator()],
        error_messages={
            'unique': "Ya existe un usuario con ese nombre.",
        },
    )
    
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    role = models.IntegerField(choices=ROLES, default=2)

    def __str__(self):
        return self.username