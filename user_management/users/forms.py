from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmar Contraseña"  # Alias personalizado para este campo
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'telefono', 'rol']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'telefono': 'Teléfono',
            'rol': 'Rol',
        }
        help_texts = {
            'username': '',  # Elimina el texto de ayuda predeterminado
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password_confirm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
