from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.views import View
from .forms import *
from django.views.generic import ListView
from .models import *
from datetime import timedelta

# Create your views here.

# limitamos el acceso segun el rol
def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Si el grupo es 'manicurista', verifica su estado de aprobación
                if group_name == 'manicurista':
                    manicurista = getattr(request.user, 'manicurista', None)
                    if manicurista:
                        if not manicurista.state:
                            # Redirige a espera_aprobacion si no está aprobado
                            return redirect('espera_aprobacion')
                        return view_func(request, *args, **kwargs)
                # Si el usuario es cliente u otro grupo
                elif request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

def home(request):

    if hasattr(request.user, 'manicurista'):
        manicurista = request.user.manicurista
        if not manicurista.state:  # Si el manicurista no está aprobado
            return redirect('espera_aprobacion')  # Redirigir a la página de espera
    

    tiposervicio = TipoServicio.objects.all()
    tipo_filtro = request.GET.get('tipo', None)
    if tipo_filtro:
        try:
            tipo_servicio_obj = TipoServicio.objects.get(nombre=tipo_filtro)
            servicio = Servicio.objects.filter(tipo_servicio=tipo_servicio_obj)
        except TipoServicio.DoesNotExist:
            servicio = Servicio.objects.none()  
    else:
        servicio = Servicio.objects.all()  

    data = {
        'servicio': servicio,
        'tiposervicio': tiposervicio
    }
    return render(request, 'app/home.html', data)



def nosotros(request):
    return render(request, 'app/nosotros.html')

def trabajaconnosotros(request):
    if request.method == 'POST':
        form = RegistroManicuristaForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            
            manicurista = Manicurista(
                user=user,
                name=form.cleaned_data['name'],
                rut=form.cleaned_data['rut'],
                profile_picture=form.cleaned_data['profile_picture'],
                certifications=form.cleaned_data['certifications'],
                state=False
            )
            manicurista.save() 

            return redirect('registroexitosom')
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
# 

# haceer reserva

@login_required
def hacer_reserva(request, servicio_id):
    servicio = get_object_or_404(Servicio, id_servicio=servicio_id)
    manicurista = servicio.manicurista
    horas_disponibles = []  # Lista de horas disponibles para el manicurista
    
    # Obtén las horas disponibles (esto depende de la lógica que implementes para manejar la disponibilidad)
    # Aquí hay un ejemplo básico de cómo podrías hacerlo. Suponiendo que el manicurista tiene un horario fijo:
    current_time = timezone.now()
    
    # Asegúrate de que el manicurista tiene horas disponibles.
    for i in range(8, 18):  # Ejemplo: 8 AM a 6 PM
        horas_disponibles.append(current_time.replace(hour=i, minute=0, second=0, microsecond=0))
    
    if request.method == 'POST':
        # Verificamos si el formulario contiene la hora seleccionada
        if 'hora_reserva' in request.POST:
            hora_reserva = request.POST.get('hora_reserva')
            # Mostrar la página de confirmación con la hora seleccionada
            return render(request, 'app/usuario/confirmar_reserva.html', {
                'hora_reserva': hora_reserva,
                'servicio': servicio,
                'manicurista': manicurista
            })
        
        # Si el usuario confirma la reserva, la guardamos en la base de datos
        if 'confirmar_reserva' in request.POST:
            hora_reserva = request.POST.get('hora_reserva')
            reserva = Reserva.objects.create(
                cliente=request.user,
                servicio=servicio,
                manicurista=manicurista,
                fecha_hora=hora_reserva,  # Usamos la hora seleccionada
                estado='pendiente',
            )
            return redirect('reserva_detalle', reserva_id=reserva.id)
    
    return render(request, 'app/reservar.html', {'servicio': servicio, 'horas_disponibles': horas_disponibles})

# probando reserva por medio de calendario

def calendario(request, id_servicio):
    return render(request, 'app/reservas/calendario.html', {'id_servicio': id_servicio})
    
def eventos(request):
    # Ejemplo: Cargar horarios disponibles para un servicio
    fecha_inicio = request.GET.get('start')
    fecha_fin = request.GET.get('end')

    if not fecha_inicio or not fecha_fin:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

#     # Parsear las fechas recibidas
    fecha_inicio = parse_datetime(fecha_inicio)
    fecha_fin = parse_datetime(fecha_fin)

    eventos = Evento.objects.filter(fecha_inicio__range=[fecha_inicio, fecha_fin])

    # Crear la lista de eventos
    eventos_json = []
    
    for evento in eventos:
        eventos_json.append({
            'title': evento.servicio.tipo_servicio.nombre + ' ' + evento.manicurista.name,
            'start': (evento.fecha_inicio + timedelta(hours=3)).isoformat(),
            'end': (evento.fecha_fin + timedelta(hours=3)).isoformat(),
            # 'start': evento.fecha_inicio.isoformat(),
            # 'end': evento.fecha_fin.isoformat(),
        })
    print(eventos_json)
    return JsonResponse(eventos_json, safe=False)

def crear_evento(request):

    fecha_inicio = request.GET.get('start')
    fecha_fin = request.GET.get('end')
    print('fecha inicio: ', fecha_inicio, 'fecha fin: ', fecha_fin)
    return JsonResponse(fecha_inicio, safe=False)

# def validar_disponibilidad(manicurista, fecha_hora):
#     reservas = Reserva.objects.filter(manicurista=manicurista, fecha_hora=fecha_hora)
#     if reservas.exists():
#         raise ValidationError("El manicurista ya tiene una reserva en ese horario.")

# def reserva_detalle(request, reserva_id):
#     reserva = get_object_or_404(Reserva, id=reserva_id)
#     return render(request, 'app/usuario/reserva_detalle.html', {'reserva': reserva})


# def reservamensual(request):
#     is_manicurista = request.user.groups.filter(name='manicurista').exists()
#     if is_manicurista:
#         manicurista = Manicurista.objects.filter(user=request.user).first()
#         if manicurista and not manicurista.state:
#             # Redirige si el manicurista no está aprobado
#             return redirect('espera_aprobacion') 
#     return render(request, 'app/manicurista/reservas/reservamensual.html',{
#         'is_manicurista': is_manicurista,
#     })

# 

def reservamensual(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            return redirect('espera_aprobacion')

    return render(request, 'app/manicurista/reservas/reservamensual.html', {
        'is_manicurista': is_manicurista,
    })



# def api_reservas(request):
#     # Simulación de reservas (en un futuro, reemplaza con datos reales de tu modelo)
#     reservas = [
#         {
#             "title": "Reserva de ejemplo",
#             "start": "2024-11-10",
#             "url": "/detallereserva/"
#         },
#         {
#             "title": "Otra reserva",
#             "start": "2024-11-12",
#             "url": "/detallereserva/"
#         },
#     ]
#     return JsonResponse(reservas, safe=False)
def api_reservas_falsas(request):
    from datetime import datetime, timedelta

    hoy = datetime.now()
    reservas_falsas = []

    for i in range(5):  # Crear 5 reservas
        dia_reserva = hoy + timedelta(days=i * 3)  # Cada 3 días
        reservas_falsas.append({
            "title": f"Reserva Falsa {i + 1}",
            "start": dia_reserva.strftime('%Y-%m-%d'),
            "url": "/detallereserva/",  # Puedes ajustar esta URL
            "className": "bg-[#DE98B1] text-white rounded-lg shadow-md hover:bg-[#C57897]"
        })

    return JsonResponse(reservas_falsas, safe=False)


def confirmar_reserva(request, servicio_id):
    # Lógica para manejar la confirmación
    return render(request, 'app/usuario/confirmar_reserva.html', {'servicio_id': servicio_id})

# 

def detallereserva(request):
    return render(request, 'app/manicurista/reservas/detallereserva.html')

def editarLocal(request, id_local):

    local = get_object_or_404(Local, id_local=id_local)

    data = {
        'form': LocalForm(instance=local)
    }

    if request.method == 'POST':
        formulario = LocalForm(data=request.POST, instance=local, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="local")
        data["form"] = formulario


    return render(request, 'app/manicurista/informacion/editarLocal.html', data)

@login_required
@group_required('manicurista')
def local(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            return redirect('espera_aprobacion')
        
    manicurista = request.user.manicurista  

    try:
        local = Local.objects.get(manicurista=manicurista)
    except Local.DoesNotExist:
        local = None 
    context = {
        'manicurista': manicurista,
        'local': local,
    }
    return render(request, 'app/manicurista/informacion/local.html', {'manicurista': manicurista, 'local': local, 'is_manicurista': is_manicurista})

@login_required
@group_required('manicurista')
def milocal(request):     
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            return redirect('espera_aprobacion')

    local = Local.objects.filter(manicurista=manicurista).select_related('local')
    data = {
        'form': LocalForm(),
        'local': local,
        'is_manicurista': is_manicurista,
    }

    if request.method == 'POST':
        formulario = LocalForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            local = formulario.save(commit=False)
            local.manicurista = manicurista
            local.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

     
    return render(request, 'app/manicurista/informacion/milocal.html', data)

@login_required
@group_required('manicurista')
def misdatos(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            return redirect('espera_aprobacion')
        
    user = request.user
    return render(request, 'app/manicurista/informacion/misdatos.html', {'user': user})

# Servicios

def misservicios(request):
    servicio = Servicio.objects.filter(manicurista=request.user).select_related('tipo_servicio')

    data = {
        'form': ServicioForm(),
        'servicio': servicio,
    }

    if request.method == 'POST':
        formulario = ServicioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            servicio = formulario.save(commit=False)
            servicio.manicurista = request.user
            servicio.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

    return render(request, 'app/manicurista/informacion/misservicios.html', data)

def modificar(request, id_servicio):

    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)

    data = {
        'form': ServicioForm(instance=servicio)
    }

    if request.method == 'POST':
        formulario = ServicioForm(data=request.POST, instance=servicio, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="misservicios")
        data["form"] = formulario

    return render(request, 'app/manicurista/serv/modificar.html', data)

def eliminar(request, id_servicio):
    servicio = get_object_or_404(Servicio, id_servicio=id_servicio)
    servicio.delete()
    return redirect(to="misservicios")

def agregarserv(request):
    data = {
        'form': TipoServicioForm()
    }

    if request.method == 'POST':
        formulario = TipoServicioForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

    return render(request, 'app/admin/crud/agregarserv.html', data)

def eliminarserv(request, id_tipo_servicio):
    tipo_servicio = get_object_or_404(TipoServicio, id_tipo_servicio=id_tipo_servicio)
    tipo_servicio.delete()
    return redirect(to="servicios")

def modificarserv(request, id_tipo_servicio):

    tipo_servicio = get_object_or_404(TipoServicio, id_tipo_servicio=id_tipo_servicio)

    data = {
        'form': TipoServicioForm(instance=tipo_servicio)
    }

    if request.method == 'POST':
        formulario = TipoServicioForm(data=request.POST, instance=tipo_servicio, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="servicios")
        data["form"] = formulario

    return render(request, 'app/admin/crud/modificarserv.html', data)



# login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        try:
            user = User.objects.get(username=username)
            # Si el usuario existe pero está inactivo
            if not user.is_active:
                messages.error(request, "Su cuenta ha sido desactivada. Por favor, contacte al administrador.")
                return render(request, 'app/login.html')
        except User.DoesNotExist:
            # Si el usuario no existe
            messages.error(request, "El nombre de usuario ingresado no existe.")
            return render(request, 'app/login.html')

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='manicurista').exists():
                print(user.groups.all())
                return redirect('reservasdia')
            elif user.groups.filter(name='cliente').exists():
                return redirect('home')
            elif user.groups.filter(name='admin').exists():
                return redirect('manicuristas')
            else:
                return redirect('home')
        else:
            # Si las credenciales son incorrectas
            messages.error(request, "La contraseña es incorrecta.")

    return render(request, 'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# ingreso requerido 
@login_required
@group_required('cliente')
def homecliente(request):
    is_cliente = request.user.groups.filter(name='cliente').exists()

    reservas = Reserva.objects.filter(cliente=request.user)
    tiposervicio = TipoServicio.objects.all()
    tipo_filtro = request.GET.get('tipo', None)
    if tipo_filtro:
        try:
            tipo_servicio_obj = TipoServicio.objects.get(nombre=tipo_filtro)
            servicio = Servicio.objects.filter(tipo_servicio=tipo_servicio_obj)
        except TipoServicio.DoesNotExist:
            servicio = Servicio.objects.none()  
    else:
        servicio = Servicio.objects.all()  

    data = {
        'servicio': servicio,
        'tiposervicio': tiposervicio
    }

    return render(request, 'app/homecliente.html', {
        'is_cliente': is_cliente,
        'reservas': reservas,
        'servicio': servicio,
        'tiposervicio': tiposervicio,
        'tipo_filtro': tipo_filtro,
        'data' : data
    })


@login_required
@group_required('manicurista')
def reservasdia(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            # Redirige si el manicurista no está aprobado
            return redirect('espera_aprobacion') 
    # Renderiza la página de reservas si está aprobado
    return render(request, 'app/manicurista/reservas/reservadia.html', {
        'is_manicurista': is_manicurista,
    })

@login_required
@group_required('admin')
def manicuristas(request):
    is_admin = request.user.groups.filter(name='admin').exists()
    # Filtra solo los manicuristas que aún no están aprobados
    manicuristas = Manicurista.objects.filter(state=False)
    return render(request, 'app/admin/manicuristas.html', {'manicuristas': manicuristas, 'is_admin': is_admin})

@login_required
@group_required('admin')
def servicios(request):
    is_admin = request.user.groups.filter(name='admin').exists()

    tipo_servicio = TipoServicio.objects.all()
    data = {
        'tipo_servicio': tipo_servicio
    }

    return render(request, 'app/admin/servicios.html', {'is_admin': is_admin, 'tipo_servicio' : tipo_servicio, 'data' : data})

@login_required
@group_required('manicurista') 
def misservicios(request):
    is_manicurista = request.user.groups.filter(name='manicurista').exists()
    if is_manicurista:
        manicurista = Manicurista.objects.filter(user=request.user).first()
        if manicurista and not manicurista.state:
            return redirect('espera_aprobacion')

    servicio = Servicio.objects.filter(manicurista=manicurista).select_related('tipo_servicio')
    data = {
        'form': ServicioForm(),
        'servicio': servicio,
        'is_manicurista': is_manicurista,
    }

    if request.method == 'POST':
        formulario = ServicioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            servicio = formulario.save(commit=False)
            servicio.manicurista = manicurista
            servicio.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario

    return render(request, 'app/manicurista/informacion/misservicios.html', data)

# aprobación manicurista

@login_required
def espera_aprobacion(request):
    if hasattr(request.user, 'manicurista'):
        manicurista = request.user.manicurista
        motivo_rechazo = manicurista.motivo_rechazo if not manicurista.state else None
        return render(request, 'app/manicurista/espera_aprobacion.html', {'motivo_rechazo': motivo_rechazo})
    return redirect('home')

@login_required
@group_required('admin')
def aprobar_manicurista(request, manicurista_id):
    manicurista = get_object_or_404(Manicurista, id=manicurista_id)
    manicurista.state = True 
    manicurista.save()

    user = manicurista.user
    user.is_active = True
    user.save()
    manicurista_group = Group.objects.get(name='manicurista')
    user.groups.add(manicurista_group)

    # messages.success(request, "El manicurista ha sido aprobado y ahora puede iniciar sesión.")
    return redirect('manicuristas')

@login_required
@group_required('admin')
def rechazar_manicurista(request, manicurista_id):
    manicurista = get_object_or_404(Manicurista, id=manicurista_id)
    
    # verifica si el manicurista ya fue rechazado previamente
    ya_rechazado = manicurista.state == False and manicurista.motivo_rechazo is not None

    # permite rechazar solo si no ha sido rechazado antes o si ha subido un nuevo certificado
    if ya_rechazado and not manicurista.certificado_actualizado:
        # mensaje si el manicurista fue rechazado antes y no hay un nuevo certificado
        return render(request, 'app/admin/rechazar_manicurista.html', {
            'manicurista': manicurista,
            'mensaje_error': "Este manicurista ya ha sido rechazado. No puedes rechazar nuevamente hasta que suba un nuevo certificado.",
            'ya_rechazado': True
        })

    if request.method == 'POST':
        # guardar el motivo del rechazo y cambiar el estado del manicurista
        motivo_rechazo = request.POST.get('motivo_rechazo')
        manicurista.motivo_rechazo = motivo_rechazo
        manicurista.state = False
        manicurista.certificado_actualizado = False 
        manicurista.save()

        return redirect('manicuristas')

    return render(request, 'app/admin/rechazar_manicurista.html', {
        'manicurista': manicurista,
        'ya_rechazado': False
    })

# actualizar certificado


@login_required
def actualizar_certificacion(request):
    manicurista = get_object_or_404(Manicurista, user=request.user)
    
    # verifica si el estado es rechazado y no ha subido un nuevo certificado
    if manicurista.state == False and not manicurista.certificado_actualizado:
        if request.method == 'POST' and 'certificacion' in request.FILES:
            manicurista.certifications = request.FILES['certificacion']
            manicurista.certificado_actualizado = True
            manicurista.save()
            return render(request, 'app/manicurista/actualizar_certificacion.html', {
                'certificado_subido': True,
            })
        return render(request, 'app/manicurista/actualizar_certificacion.html', {
            'certificado_subido': False,
        })
    
    # si el certificado ya se actualizo o la solicitud no ha sido rechazado
    return render(request, 'app/manicurista/actualizar_certificacion.html', {
        'certificado_subido': None,
    })

# Calendario
class CalendarioView(ListView):
    model = Reserva
    template_name = "app/calendario.html"

def reserServ (request):
    manicurista = Manicurista.objects.all()  
    servicio = Servicio.objects.all()

    data = {
        'manicurista': manicurista,
        'servicio': servicio,
    }
    return render(request, 'app/reserServ.html', data)
