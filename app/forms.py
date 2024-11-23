# en tu_app/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import Manicurista, Servicio, TipoServicio, Reserva, Local


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_hora']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Repetir Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            cliente_group, created = Group.objects.get_or_create(name='cliente')
            user.groups.add(cliente_group)

        return user
User = get_user_model()

class RegistroManicuristaForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    rut = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=True)
    certifications = forms.FileField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Solo campos del modelo User
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        # Crear el usuario
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            # Crear el perfil de Manicurista relacionado con el usuario
            Manicurista.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                rut=self.cleaned_data['rut'],
                profile_picture=self.cleaned_data['profile_picture'],
                certifications=self.cleaned_data['certifications'],
                state=False  # Inicia como no aprobado
            )
        return user

    # 

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['tipo_servicio', 'valor',]

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = '__all__'

# class ManicuristaForm(forms.ModelForm):
#     class Meta:
#         model = Manicurista
#         fields = '__all__'


class ActualizarCertificacionForm(forms.ModelForm):
    class Meta:
        model = Manicurista
        fields = ['certifications'] 


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nombre', 'numero_telefono', 'direccion', 'comuna',]


class ManicuristaForm(forms.ModelForm):
    class Meta:
        model = Manicurista
        fields = ['name', 'rut', 'profile_picture',]