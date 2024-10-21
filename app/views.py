from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    return render(request, 'app/home.html')

def nosotros(request):
    return render(request, 'app/nosotros.html')
def trabajaconnosotros(request):
    return render(request, 'app/manicurista/trabajaconnosotros.html')

def registrotrabajador(request):
    return render(request, 'app/manicurista/registrotrabajador.html')

def registroexitosom(request):
    return render(request, 'app/manicurista/registroexitosom.html')

def infoprofesional(request):
    return render(request, 'app/manicurista/infoprofesional.html')

def reservasdia(request):
    return render(request, 'app/manicurista/reservas/reservadia.html')

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

def login_view(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')