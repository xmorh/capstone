# from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import Group,User
from .forms import RegistroClienteForm, RegistroManicuristaForm
from .models import Manicurista

# Create your views here.

# limitamos el acceso segun el rol
def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied 
        return _wrapped_view
    return decorator

def home(request):
    return render(request, 'app/home.html')

def nosotros(request):
    return render(request, 'app/nosotros.html')

def trabajaconnosotros(request):
    if request.method == 'POST':
        form = RegistroManicuristaForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_user_model().objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            
            Manicurista.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                rut=form.cleaned_data['rut'],
                profile_picture=form.cleaned_data['profile_picture'],
                certifications=form.cleaned_data['certifications'],
            )
            manicurista_group = Group.objects.get(name='manicurista')
            user.groups.add(manicurista_group)
            login(request, user)
            
            return redirect('registroexitosom')
        else:
            messages.error(request, "Hubo un error en el registro. Por favor, verifica los datos.")
    else:
        form = RegistroManicuristaForm()
    
    return render(request, 'app/manicurista/trabajaconnosotros.html', {'form': form})

def registroexitosom(request):
    return render(request, 'app/manicurista/registroexitosom.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homecliente')
        else:
            messages.error(request, "Hubo un error al crear la cuenta. Verifica los datos ingresados.")
    else:
        form = RegistroClienteForm()
    return render(request, 'app/registrocliente.html', {'form': form})

def infoprofesional(request):
    return render(request, 'app/manicurista/infoprofesional.html')

def misreservas(request):
    return render(request, 'app/usuario/misreservas.html')

def reservamensual(request):
    # manicurista_group = Group.objects.get(name='manicurista')
    # manicuristas = User.objects.filter(groups=manicurista_group)
    return render(request, 'app/manicurista/reservas/reservamensual.html')



def detallereserva(request):
    return render(request, 'app/manicurista/reservas/detallereserva.html')

def milocal(request):
    return render(request, 'app/manicurista/informacion/milocal.html')

def misdatos(request):
    return render(request, 'app/manicurista/informacion/misdatos.html')

def misservicios(request):
    return render(request, 'app/manicurista/informacion/misservicios.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='manicurista').exists():
                print(user.groups.all())
                return redirect('reservasdia')
            elif user.groups.filter(name='cliente').exists():
                return redirect('homecliente')
            elif user.groups.filter(name='admin').exists():
                return redirect('manicuristas')
            else:
                return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ingreso requerido 
@login_required
@group_required('cliente')
def homecliente(request):
    is_cliente = request.user.groups.filter(name='cliente').exists()
    return render(request, 'app/home.html', {
        'is_cliente': is_cliente,
    })


@login_required
@group_required('manicurista')
def reservasdia(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    return render(request, 'app/manicurista/reservas/reservadia.html', {
        'is_manicurista': is_manicurista,
    })

@login_required
@group_required('admin')
def manicuristas(request):
    # definimos para poder mostrar los link y definir que se utilizara en la pagina
    is_admin = request.user.groups.filter(name='admin').exists()
    manicurista_group = Group.objects.get(name='manicurista')
    manicuristas = User.objects.filter(groups=manicurista_group).select_related('manicurista')
    return render(request, 'app/admin/manicuristas.html', {'manicuristas': manicuristas ,'is_admin': is_admin})

@login_required
@group_required('admin')
def servicios(request):
    is_admin = request.user.groups.filter(name='admin').exists()
    return render(request, 'app/admin/servicios.html', {'is_admin': is_admin})


