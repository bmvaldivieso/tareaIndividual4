from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string

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
    email_verified = models.BooleanField(default=False)  
    verification_token = models.CharField(max_length=64, blank=True, null=True)  
    
    class Meta:
        db_table = 'usuario'

    def generate_verification_token(self):
        """Generar un token único para la verificación."""
        self.verification_token = get_random_string(length=64)
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.rol}"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'cliente'})
    direccion = models.TextField(blank=True, null=True)
    peso = models.CharField(max_length=15, blank=True, null=True)
    edad = models.CharField(max_length=15, blank=True, null=True)
    altura = models.CharField(max_length=15, blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return f"Cliente: {self.user.username}"


class Entrenador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'rol': 'entrenador'})
    especialidad = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)
    experiencia_laboral = models.CharField(max_length=15, blank=True, null=True)
    idioma1 = models.CharField(max_length=15, blank=True, null=True)
    idioma2 = models.CharField(max_length=15, blank=True, null=True)
    cargo = models.CharField(max_length=20, blank=True, null=True)

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

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('Ocupado', 'Ocupado'),
        ('Desocupado', 'Desocupado')
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()  # Fecha de la reserva
    hora = models.TimeField()  # Hora de la reserva
    actividad = models.CharField(max_length=100)  # Actividad reservada
    duracion = models.CharField(max_length=50, default="1 hora")  # Duración (1 hora fija)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='Ocupado'
    )  # Estado de la reserva (ocupado o desocupado)

    class Meta:
        db_table = 'reserva'

    def __str__(self):
        return f"{self.actividad} - {self.fecha} a las {self.hora}"

    def actualizar_estado(self):
        """Actualizar el estado a 'Desocupado' si la hora ya pasó"""
        if self.fecha < now().date() or (self.fecha == now().date() and self.hora < now().time()):
            self.estado = 'Desocupado'
            self.save()

class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField()

    def is_valid(self):
        current_time = timezone.now()
        print(f"Hora de creación (local): {timezone.localtime(self.created_at)}")
        print(f"Hora actual (local): {timezone.localtime(current_time)}")
        return current_time < self.created_at + timedelta(minutes=5)
    
class Clase(models.Model):
    entrenador = models.ForeignKey(Entrenador, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    duracion = models.DurationField()
    capacidad = models.IntegerField()

    class Meta:
        db_table = 'clase'

    def __str__(self):
        return f"Clase: {self.nombre} - Entrenador: {self.entrenador.user.username}"

class Asignacion(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asignacion'

    def __str__(self):
        return f"Asignacion: {self.cliente.user.username} a la clase {self.clase.nombre}"    





