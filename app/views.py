from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import RegistroClienteForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

@login_required
def homecliente(request):
    is_cliente = request.user.groups.filter(name='cliente').exists()
    return render(request, 'app/home.html', {
        'is_cliente': is_cliente,
    })

def nosotros(request):
    return render(request, 'app/nosotros.html')
def trabajaconnosotros(request):
    return render(request, 'app/manicurista/trabajaconnosotros.html')

def registrotrabajador(request):
    return render(request, 'app/manicurista/registrotrabajador.html')

def registroexitosom(request):
    return render(request, 'app/manicurista/registroexitosom.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, "Cuenta creada exitosamente.") no es necesario ya que se redirige a home de cliente
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

@login_required
def reservasdia(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    return render(request, 'app/manicurista/reservas/reservadia.html', {
        'is_manicurista': is_manicurista,
    })

def manicuristas(request):
    return render(request, 'app/admin/manicuristas.html')

def reservamensual(request):
    return render(request, 'app/manicurista/reservas/reservamensual.html')

def detallereserva(request):
    return render(request, 'app/manicurista/reservas/detallereserva.html')

def milocal(request):
    return render(request, 'app/manicurista/informacion/milocal.html')

def misdatos(request):
    return render(request, 'app/manicurista/informacion/misdatos.html')

def misservicios(request):
    return render(request, 'app/manicurista/informacion/misservicios.html')

# autenticación
# def create_groups():
#     Group.objects.get_or_create(name='manicurista')
#     Group.objects.get_or_create(name='cliente')

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
            else:
                return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




