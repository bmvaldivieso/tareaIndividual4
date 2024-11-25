
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('entrenador/dashboard/', views.entrenador_dashboard, name='entrenador_dashboard'),
    path('gerente/dashboard/', views.gerente_dashboard, name='gerente_dashboard'),
    path('clientepage/', views.cliente_page, name='cliente_page'),
    path('gestion/', views.gestion, name='gestion'),
]



