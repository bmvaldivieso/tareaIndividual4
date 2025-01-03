from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):  
    ADMIN = 'administrador'
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('entrenador', 'Entrenador'),
        ('gerente', 'Gerente'),
        (ADMIN, 'Administrador'),
    ]

    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rol}"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'cliente'})
    direccion = models.TextField(blank=True, null=True)
    peso = models.CharField(max_length=15, blank=True, null=True)
    edad = models.CharField(max_length=15, blank=True, null=True)
    altura = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"Cliente: {self.user.username}"


class Entrenador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'entrenador'})
    especialidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'entrenador'

    def __str__(self):
        return f"Entrenador: {self.user.username}"


class Gerente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'gerente'})
    area_responsable = models.CharField(max_length=100)

    class Meta:
        db_table = 'gerente'

    def __str__(self):
        return f"Gerente: {self.user.username}"
    
class EvaluacionFisica(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    peso = models.FloatField(validators=[MinValueValidator(0.0)])
    porcentaje_grasa = models.FloatField(validators=[MinValueValidator(0.0)])
    resistencia_fisica = models.CharField(max_length=100)
    fecha_registro = models.DateField(db_index=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'evaluacionfisica'

    def __str__(self):
        return f"{self.user.username} - {self.record_date}"   

