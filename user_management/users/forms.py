from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Cliente, EvaluacionFisica, Entrenador

class RegistrationForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False, label='Dirección')
    peso = forms.CharField(max_length=15, required=False, label='Peso')
    altura = forms.CharField(max_length=15, required=False, label='Altura')
    edad = forms.CharField(max_length=15, required=False, label='Edad')
    cedula = forms.CharField(max_length=15, required=False, label='Cedula')

    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nombre de usuario', 
        widget=forms.TextInput(attrs={'aria-label': 'Nombre de usuario'}),
        error_messages={'required': '', 'max_length': ''} 
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'aria-label': 'Contraseña', 'placeholder': 'Contraseña'}),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'La contraseña debe contener al menos 8 caracteres.',
            'password_too_similar': 'Tu contraseña no puede ser demasiado similar a tu otra información personal.',
            'common_password': 'La contraseña no puede ser una contraseña comúnmente usada.',
            'numeric_password': 'La contraseña no puede ser completamente numérica.',
        }
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'aria-label': 'Confirmar contraseña', 'placeholder': 'Confirmar contraseña'}),
        error_messages={'required': 'Este campo es obligatorio.'}
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'peso', 'altura', 'edad', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'cedula': 'Cédula',
        }

    def save(self, commit=True):
        # Guarda el usuario principal
        user = super().save(commit=False)
        user.rol = 'cliente'  # Asigna el rol por defecto
        if commit:
            user.save()
            # Crea una instancia de Cliente asociada al usuario
            Cliente.objects.create(
                user=user,
                direccion=self.cleaned_data.get('direccion', ''),
                peso=self.cleaned_data.get('peso', ''),
                altura=self.cleaned_data.get('altura', ''),
                edad=self.cleaned_data.get('edad', ''),
                cedula=self.cleaned_data.get('cedula', ''),
            )
        return user

    def clean_username(self):
        # Si es una edición, no validamos la unicidad del username
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.username == username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class EvaluationFisicaForm(forms.ModelForm):
    class Meta:
        model = EvaluacionFisica
        fields = ['peso', 'porcentaje_grasa', 'resistencia_fisica', 'fecha_registro', 'notas_adicionales']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'notas_adicionales': forms.Textarea(attrs={
                'rows': 6,  # Número de filas
                'cols': 40,  # Número de columnas
            }),
        }
        labels = {
            'peso': 'Peso',
            'porcentaje_grasa': 'Porcentaje de Grasa',
            'resistencia_fisica': 'Resistencia Física',
            'fecha_registro': 'Fecha del Registro',
            'notas_adicionales': 'Notas Adicionales',
        }
        help_texts = {
            'peso': 'Ingrese su peso en kilogramos.',
            'porcentaje_grasa': 'Ingrese el porcentaje de grasa corporal.',
            'resistencia_fisica': 'Describa su nivel de resistencia física.',
            'fecha_registro': 'Seleccione la fecha en que se realizó la evaluación.',
            'notas_adicionales': 'Agregue cualquier información adicional relevante (opcional).',
        }

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso <= 0:
            raise forms.ValidationError("El peso debe ser un número positivo.")
        return peso

    def clean_porcentaje_grasa(self):
        porcentaje_grasa = self.cleaned_data.get('porcentaje_grasa')
        if porcentaje_grasa < 0 or porcentaje_grasa > 100:
            raise forms.ValidationError("El porcentaje de grasa debe estar entre 0 y 100.")
        return porcentaje_grasa
    
class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = ['especialidad', 'direccion', 'cedula', 'experiencia_laboral', 'idioma1', 'idioma2', 'cargo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ciudad donde reside'}),
            'especialidad': forms.TextInput(attrs={'placeholder': 'Musculación, cardio, yoga'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Numero de cédula'}),
            'experiencia_laboral': forms.TextInput(attrs={'placeholder': 'Años de experiencia'}),
            'idioma1': forms.TextInput(attrs={'placeholder': 'Que domina'}),
            'idioma2': forms.TextInput(attrs={'placeholder': 'Que domina'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Que estaria interesado'}),
        }

class UserEntrenadorForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nombre de usuario', 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        error_messages={'required': '', 'max_length': ''} 
    )
    
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'aria-label': 'Contraseña', 'placeholder': 'Contraseña'}),
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'La contraseña debe contener al menos 8 caracteres.',
            'password_too_similar': 'Tu contraseña no puede ser demasiado similar a tu otra información personal.',
            'common_password': 'La contraseña no puede ser una contraseña comúnmente usada.',
            'numeric_password': 'La contraseña no puede ser completamente numérica.',
        }
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'aria-label': 'Confirmar contraseña', 'placeholder': 'Confirmar contraseña'}),
        error_messages={'required': 'Este campo es obligatorio.'}
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'cedula': 'Cédula',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'entrenador'  # Asignar el rol automáticamente
        user.set_password(self.cleaned_data['password1'])  # Establecer la contraseña
        if commit:
            user.save()
        return user      


          
    
    