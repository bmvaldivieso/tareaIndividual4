from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('entrenador', 'Entrenador'),
        ('gerente', 'Gerente'),
        ('administrador', 'Administrador'),
    ]

    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rol}"
