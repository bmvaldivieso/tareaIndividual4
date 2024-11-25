from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import User, Cliente
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('login')
            except Exception as e:
                form.add_error(None, f"Ocurrió un error al registrar: {str(e)}")
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'gestion')  # Redirige a 'next' si está definido
                return redirect(next_url)
            else:
                form.add_error(None, "Credenciales incorrectas.")
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def gestion(request):
    rol = getattr(request.user, 'rol', None)  # Usa getattr para evitar errores si 'rol' no existe
    if rol == 'cliente':
        return redirect('cliente_page')
    elif rol == 'entrenador':
        return redirect('entrenador_dashboard')
    elif rol == 'gerente':
        return redirect('gerente_dashboard')
    else:
        return render(request, 'users/error.html', {'message': 'Rol desconocido o no asignado.'})

@login_required
def cliente_page(request):
    # Verifica si el usuario logueado tiene el rol 'cliente'
    if hasattr(request.user, 'rol') and request.user.rol == 'cliente': 
        # Obtenemos el cliente correspondiente al usuario logueado
        cliente = Cliente.objects.get(user=request.user)  # Asegúrate de que 'user' es una relación correcta
        return render(request, 'users/cliente_page.html', {'cliente': cliente})
    
@login_required
def entrenador_dashboard(request):
    if request.user.rol != 'entrenador':  # Verifica directamente el rol
        return redirect('gestion')
    return render(request, 'users/entrenador_dashboard.html', {'user': request.user})

@login_required
def gerente_dashboard(request):
    if request.user.rol != 'gerente':  # Verifica directamente el rol
        return redirect('gestion')
    return render(request, 'users/gerente_dashboard.html', {'user': request.user})   

def is_cliente(user):
    return user.rol == 'cliente'

@login_required
@user_passes_test(is_cliente)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    cliente = get_object_or_404(Cliente, user=user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            # Guardar el usuario
            user = form.save(commit=False)

            # Verificar si se proporciona una nueva contraseña
            if form.cleaned_data['password1']:
                user.password = make_password(form.cleaned_data['password1'])  # Cifrar la contraseña

            user.save()

            # Vuelve a autenticar al usuario si la contraseña cambió
            login(request, user)  # Esto es clave

            # Actualizar los datos de Cliente
            cliente.direccion = form.cleaned_data['direccion']
            cliente.peso = form.cleaned_data['peso']
            cliente.altura = form.cleaned_data['altura']
            cliente.edad = form.cleaned_data['edad']
            cliente.save()

            return redirect('cliente_page')
    else:
        form = RegistrationForm(instance=user)
        form.initial['direccion'] = cliente.direccion
        form.initial['peso'] = cliente.peso
        form.initial['altura'] = cliente.altura
        form.initial['edad'] = cliente.edad

    return render(request, 'users/edit_user.html', {'form': form, 'user': user})