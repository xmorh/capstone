from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('nosotros', nosotros, name='nosotros'),
    path('trabajaconnosotros', trabajaconnosotros, name='trabajaconnosotros'),
    path('login', login, name='login'),
    path('registrotrabajador', registrotrabajador, name='registrotrabajador'),
    path('registroexitosom', registroexitosom, name='registroexitosom'),
    path('reservasdia', reservasdia, name='reservasdia'),
    path('reservamensual', reservamensual, name='reservamensual'), 
    path('detallereserva', detallereserva, name='detallereserva'), 
    path('infoprofesional', infoprofesional, name='infoprof'),
    path('misservicios', misservicios, name='misservicios'),
    path('misdatos', misdatos, name='misdatos'),
    path('milocal', milocal, name='milocal'),
    path('reservas', reservas, name='reservas'),
    path('detalle', detalle, name='detalle'),
    path('user', user, name='user')
]
