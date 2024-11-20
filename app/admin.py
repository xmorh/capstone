from django.contrib import admin
from app.models import Manicurista, Servicio, TipoServicio, Reserva, Evento


# Register your models here.

# class ManicuristaAdmin(admin.ModelAdmin):
#     list_display = ('id','run_m', 'nombre','email', 'password','telefono', 'direccion', 'foto', 'certificacion')

class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id_servicio','valor', 'tipo_servicio')
    list_filter = ('tipo_servicio',)

# class ReservaAdmin(admin.ModelAdmin):
#     list_display = ('id_reserva','horario', 'manicurista','servicio', 'cliente')

class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_servicio','nombre', 'duracion', 'descripcion')
    list_filter = ('nombre',)

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'servicio', 'manicurista', 'inicio', 'fin', 'descripcion')
    list_filter = ('inicio', 'manicurista')
    search_fields = ('titulo', 'descripcion')
    list_per_page = 10

admin.site.register(Reserva)
admin.site.register(Manicurista)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(TipoServicio,TipoServicioAdmin)
admin.site.register(Evento, EventoAdmin)

