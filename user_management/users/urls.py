from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    EvaluacionFisicaCreate,
    EvaluacionFisicaList,
    EvaluacionFisicaUpdate,
)
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('entrenador/dashboard/', views.entrenador_dashboard, name='entrenador_dashboard'),
    path('clientepage/', views.cliente_page, name='cliente_page'),
    path('gestion/', views.gestion, name='gestion'),
    path('evaluaciones/', EvaluacionFisicaList.as_view(), name='evaluaciones_list'),
    path('evaluaciones/nueva/', EvaluacionFisicaCreate.as_view(), name='evaluacionfisica_create'),
    path('evaluaciones/<int:pk>/editar/', EvaluacionFisicaUpdate.as_view(), name='evaluacionfisica_update'),
    path('gerente_cliente/', views.gerente_cliente, name='gerente_cliente'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('registrar_entrenador/', views.registrar_entrenador, name='registrar_entrenador'),
    path('gerente_entrenador/', views.gerente_entrenador, name='gerente_entrenador'),
    path('listar_reservas/', views.listar_reservas, name='listar_reservas'),
    path('listar_reservas/nueva/', views.nueva_reserva, name='nueva_reserva'),
    path('listar_reservas/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('gerente/dashboard/', views.gerente_dashboard, name='gerente_dashboard'),
     # Rutas recuperar contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Ruta 2FA
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    # Verificar correo 
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
] 




