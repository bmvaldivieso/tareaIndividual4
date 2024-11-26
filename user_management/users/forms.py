from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Cliente

class RegistrationForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False, label='Dirección')
    peso = forms.CharField(max_length=15, required=False, label='Peso')
    altura = forms.CharField(max_length=15, required=False, label='Altura')
    edad = forms.CharField(max_length=15, required=False, label='Edad')

    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nombre de usuario', 
        widget=forms.TextInput(attrs={'aria-label': 'Nombre de usuario', 'placeholder': 'Nombre de usuario'}),
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
                edad=self.cleaned_data.get('edad', '')
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
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)