from django import forms
from .models import User, Cliente, Entrenador, Gerente
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['direccion']

class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = ['especialidad']

class GerenteForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = ['area_responsable']

@login_required
def cliente_edit(request):
    """
    Permite a un cliente editar su información específica.
    """
    if not hasattr(request.user, 'cliente'):
        return redirect('dashboard')  # Redirige si no es un cliente

    cliente = request.user.cliente
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_dashboard')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'users/cliente_edit.html', {'form': form})

@login_required
def entrenador_edit(request):
    """
    Permite a un entrenador editar su información específica.
    """
    if not hasattr(request.user, 'entrenador'):
        return redirect('dashboard')  # Redirige si no es un entrenador

    entrenador = request.user.entrenador
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, instance=entrenador)
        if form.is_valid():
            form.save()
            return redirect('entrenador_dashboard')
    else:
        form = EntrenadorForm(instance=entrenador)

    return render(request, 'users/entrenador_edit.html', {'form': form})


@login_required
def gerente_edit(request):
    """
    Permite a un gerente editar su información específica.
    """
    if not hasattr(request.user, 'gerente'):
        return redirect('dashboard')  # Redirige si no es un gerente

    gerente = request.user.gerente
    if request.method == 'POST':
        form = GerenteForm(request.POST, instance=gerente)
        if form.is_valid():
            form.save()
            return redirect('gerente_dashboard')
    else:
        form = GerenteForm(instance=gerente)

    return render(request, 'users/gerente_edit.html', {'form': form})
