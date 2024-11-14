from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('homecliente', homecliente, name='homecliente'),
    path('nosotros', nosotros, name='nosotros'),
    path('trabajaconnosotros', trabajaconnosotros, name='trabajaconnosotros'),
    path('registroexitosom', registroexitosom, name='registroexitosom'),
    path('registro', registro, name='registro'),
    path('reservasdia', reservasdia, name='reservasdia'),
    # 
    path('manicuristas', manicuristas, name='manicuristas'),
    path('panel/aprobar-manicurista/<int:manicurista_id>/', aprobar_manicurista, name='aprobar_manicurista'),
    path('rechazar-manicurista/<int:manicurista_id>/', rechazar_manicurista, name='rechazar_manicurista'),
    path('espera_aprobacion', espera_aprobacion, name='espera_aprobacion'),
    path('actualizar_certificacion/', actualizar_certificacion, name='actualizar_certificacion'),
    # 
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
    path('modificar/<id_servicio>/', modificar, name='modificar'),
    path('eliminar/<id_servicio>/', eliminar, name='eliminar'), 
    path('agregarserv', agregarserv, name='agregarserv'),
    path('eliminarserv/<id_tipo_servicio>/', eliminarserv, name='eliminarserv'), 
    path('modificarserv/<id_tipo_servicio>/', modificarserv, name='modificarserv'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)