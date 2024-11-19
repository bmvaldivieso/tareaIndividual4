from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import RegistrationForm, LoginForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Inicia sesión al usuario
                next_url = request.GET.get('next', 'user_table')  # Si 'next' está en la URL, redirige allí, si no, a 'user_table'
                return redirect(next_url)
            else:
                form.add_error(None, "Credenciales incorrectas.")
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_table(request):
    # Verificar si el usuario está autenticado antes de acceder al atributo 'rol'
    if request.user.is_authenticated:
        print(f"El rol del usuario es: {request.user.rol}")
    else:
        print("El usuario no está autenticado.")
    
    users = User.objects.all()
    return render(request, 'users/user_table.html', {'users': users})

def is_admin(user):
    return user.rol == 'administrador'

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_table')
    else:
        form = RegistrationForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_table')


