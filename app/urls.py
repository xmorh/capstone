from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('homecliente', homecliente, name='homecliente'),
    path('nosotros', nosotros, name='nosotros'),
    path('trabajaconnosotros', trabajaconnosotros, name='trabajaconnosotros'),
    path('registrotrabajador', registrotrabajador, name='registrotrabajador'),
    path('registroexitosom', registroexitosom, name='registroexitosom'),
    path('registro', registro, name='registro'),
    path('reservasdia', reservasdia, name='reservasdia'),
    path('manicuristas', manicuristas, name='manicuristas'),
    path('reservamensual', reservamensual, name='reservamensual'), 
    path('detallereserva', detallereserva, name='detallereserva'), 
    path('infoprofesional', infoprofesional, name='infoprof'),
    path('misservicios', misservicios, name='misservicios'),
    path('misdatos', misdatos, name='misdatos'),
    path('milocal', milocal, name='milocal'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('misreservas/', misreservas, name='misreservas'),

]
