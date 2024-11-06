# en tu_app/forms.py
from django import forms
from django.contrib.auth.models import User, Group
# from .models import CustomUser

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
    
class RegistroManicuristaForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    rut = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=True)
    certifications = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'rut', 'profile_picture', 'certifications']
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        return user 