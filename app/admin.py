from django.contrib import admin
from app.models import Manicurista, Servicio, TipoServicio


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


admin.site.register(Manicurista)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(TipoServicio,TipoServicioAdmin)

