from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Cliente, EvaluacionFisica, Entrenador
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

class RegistrationForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False, label='Dirección', widget=forms.Textarea(attrs={'rows': 3,'placeholder': 'Ciudad donde reside'}))
    peso = forms.CharField(max_length=15, required=False, label='Peso', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su peso (en kilogramos)'}))
    altura = forms.CharField(max_length=15, required=False, label='Altura', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su talla (en metros)'}))
    edad = forms.CharField(max_length=15, required=False, label='Edad', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su edad'}))
    cedula = forms.CharField(max_length=15, required=False, label='Cedula', widget=forms.TextInput(attrs={'placeholder': 'Ingrese su numero de cédula'}))

    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nombre de usuario', 
        widget=forms.TextInput(attrs={'aria-label': 'Nombre de usuario', 'placeholder': 'Evite caracteres especiales (Max. 8 digitos)'}),
        error_messages={'required': '', 'max_length': ''} 
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'aria-label': 'Contraseña', 'placeholder': 'En la contraseña no debe incluir el usuario'}),
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
        widget=forms.PasswordInput(attrs={'aria-label': 'Confirmar contraseña', 'placeholder': 'En la contraseña no debe incluir el usuario'}),
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
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingrese su Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingrese su Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su numero Teléfono'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'cliente'  # Rol por defecto
        user.email_verified = False  # Inicialmente no verificado
        if commit:
            user.save()
            user.generate_verification_token()  # Genera el token después de guardar
            # Crea la instancia de Cliente asociada
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
        username = self.cleaned_data.get('username')
        
        # Si es una edición, no validamos la unicidad del username
        if self.instance and self.instance.username == username:
            if not username.isalnum() or len(username) > 8:
                raise forms.ValidationError("El nombre de usuario no puede contener símbolos especiales y debe tener máximo 8 caracteres.")
            return username
        
        # Validar unicidad del nombre de usuario
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        
        # Validar formato del nombre de usuario
        if not username.isalnum() or len(username) > 8:
            raise forms.ValidationError("El nombre de usuario no puede contener símbolos especiales y debe tener máximo 8 caracteres.")
        
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return first_name.capitalize()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido solo puede contener letras.")
        return last_name.capitalize()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        # Opcional: restringir dominios permitidos
        allowed_domains = ['gmail.com', 'outlook.com', 'yahoo.com']
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError(f"El dominio del correo no está permitido. Usa uno de estos: {', '.join(allowed_domains)}.")
        return email
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe contener exactamente 10 dígitos y no incluir caracteres especiales.")
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion.replace(' ', '').isalpha():
            raise forms.ValidationError("La dirección solo puede contener letras y espacios.")
        if len(direccion) > 30:
            raise forms.ValidationError("La dirección no puede exceder los 30 caracteres.")
        return direccion

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if not peso.isdigit() or int(peso) > 50:
            raise forms.ValidationError("El peso debe ser un número positivo menor o igual a 50 kg.")
        return peso

    def clean_altura(self):
        altura = self.cleaned_data.get('altura')
        try:
            altura = float(altura)
            if altura <= 0 or altura > 3:
                raise forms.ValidationError("La altura debe ser positiva y menor o igual a 3 metros.")
        except ValueError:
            raise forms.ValidationError("La altura debe ser un número válido.")
        return altura

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if not edad.isdigit() or int(edad) < 0 or int(edad) > 100:
            raise forms.ValidationError("La edad debe ser un número positivo menor o igual a 100.")
        return edad

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("La cédula debe contener exactamente 10 dígitos.")
        # Aquí lógica para validar cédulas ecuatorianas
        return cedula

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
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingrese su numero de cédula (Obligatorio)'}),
            'experiencia_laboral': forms.TextInput(attrs={'placeholder': 'Años de experiencia'}),
            'idioma1': forms.TextInput(attrs={'placeholder': 'Que domina'}),
            'idioma2': forms.TextInput(attrs={'placeholder': 'Que domina'}),
            'cargo': forms.TextInput(attrs={'placeholder': 'Que estaria interesado'}),
        }

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion.replace(' ', '').isalpha():
            raise forms.ValidationError("La dirección solo puede contener letras y espacios.")
        if len(direccion) > 30:
            raise forms.ValidationError("La dirección no puede exceder los 30 caracteres.")
        return direccion
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("La cédula debe contener exactamente 10 dígitos.")
        # Aquí lógica para validar cédulas ecuatorianas
        return cedula

    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        
        if not especialidad.isalnum() or len(especialidad) > 20:
            raise forms.ValidationError("La especialidad no puede contener símbolos especiales y debe tener máximo 2 caracteres.")
        
        return especialidad

    def clean_experiencia_laboral(self):
        experiencia_laboral = self.cleaned_data.get('experiencia_laboral')
        
        if not experiencia_laboral.isalnum() or int(experiencia_laboral) < 0 or int(experiencia_laboral) > 40:
            raise forms.ValidationError("La experiencia laboral no puede contener símbolos especiales y debe ser un número positivo menor o igual a 40.")
        
        return experiencia_laboral

    def clean_idioma1(self):
        idioma1 = self.cleaned_data.get('idioma1')
        if not idioma1.isalpha():
            raise forms.ValidationError("El idioma solo puede contener letras.")
        return idioma1

    def clean_idioma2(self):
        idioma2 = self.cleaned_data.get('idioma2')
        if not idioma2.isalpha():
            raise forms.ValidationError("El idioma solo puede contener letras.")
        return idioma2
        
    def clean_cargo(self):
        cargo = self.cleaned_data.get('cargo')
        if not cargo.isalpha():
            raise forms.ValidationError("El cargo solo puede contener letras.")
        return cargo

class UserEntrenadorForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nombre de usuario', 
        widget=forms.TextInput(attrs={'aria-label': 'Nombre de usuario:', 'placeholder': 'Evite caracteres especiales (Max. 8 digitos)'}),
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
            'first_name': forms.TextInput(attrs={'placeholder': 'Ingrese su Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ingrese su Apellido'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su Correo electrónico'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese su numero Teléfono'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        
        if not username.isalnum() or len(username) > 8:
            raise forms.ValidationError("El nombre de usuario no puede contener símbolos especiales y debe tener máximo 8 caracteres.")
        
        return username
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return first_name.capitalize()
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("El apellido solo puede contener letras.")
        return last_name.capitalize()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Introduce un correo electrónico válido.")
        # Opcional: restringir dominios permitidos
        allowed_domains = ['gmail.com', 'outlook.com', 'yahoo.com']
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError(f"El dominio del correo no está permitido. Usa uno de estos: {', '.join(allowed_domains)}.")
        return email
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 10:
            raise forms.ValidationError("El teléfono debe contener exactamente 10 dígitos y no incluir caracteres especiales.")
        return telefono

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'entrenador'  # Asignar el rol automáticamente
        user.set_password(self.cleaned_data['password1'])  # Establecer la contraseña
        if commit:
            user.save()
        return user    

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        # Asunto
        subject = "Recupera tu contraseña en GymApp"

        # Cuerpo del mensaje
        email_body = render_to_string('emails/password_reset_email.html', context)

        # Enviar el correo
        email = EmailMessage(subject, email_body, from_email, [to_email])
        email.content_subtype = "html"  # Indica que el correo es HTML
        email.send()

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             use_https=False,
             token_generator=default_token_generator,
             from_email=None,
             request=None,
             html_email_template_name=None,
             extra_email_context=None):

        for user in self.get_users(self.cleaned_data['email']):
            context = {
                'email': user.email,
                'domain': domain_override or request.get_host(),
                'site_name': 'Mi Sitio Web',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            if extra_email_context is not None:
                context.update(extra_email_context)
            self.send_mail(subject_template_name, email_template_name, context, from_email, user.email, html_email_template_name)

class OTPForm(forms.Form):
    otp = forms.CharField(label="Código de Verificación", max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))



          
    
    