from django.contrib import admin
from .models import User, Cliente, Entrenador, Gerente

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'direccion')

@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad')

@admin.register(Gerente)
class GerenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'area_responsable')




