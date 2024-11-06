from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

# handler403 = 'app.views.permission_denied_view'

urlpatterns = [
    path('', home, name='home'),
    path('homecliente', homecliente, name='homecliente'),
    path('nosotros', nosotros, name='nosotros'),
    path('trabajaconnosotros', trabajaconnosotros, name='trabajaconnosotros'),
    path('registroexitosom', registroexitosom, name='registroexitosom'),
    path('registro', registro, name='registro'),
    path('reservasdia', reservasdia, name='reservasdia'),
    path('manicuristas', manicuristas, name='manicuristas'),
    path('servicios', servicios, name='servicios'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)