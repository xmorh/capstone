from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def nosotros(request):
    return render(request, 'app/nosotros.html')

def login(request):
    return render(request, 'app/login.html')

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

def reservas(request):
    return render(request, 'app/usuario/reservas.html')

def detalle(request):
    return render(request, 'app/usuario/detalle.html')

def user(request):
    return render(request, 'app/usuario/user.html')