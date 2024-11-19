from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Reserva(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    manicurista = models.ForeignKey('Manicurista', on_delete=models.CASCADE, null=True, blank=True)  # Manicurista asignado
    fecha_hora = models.DateTimeField()
    estado = models.CharField(
        max_length=20, 
        choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada')], 
        default='pendiente'
    )
    
    def __str__(self):
        return f"Reserva de {self.cliente} para {self.servicio} con {self.manicurista} el {self.fecha_hora}"

class TipoServicio(models.Model):
    id_tipo_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250, default=' ')

    def __str__(self):
        return self.nombre
    
class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    valor = models.IntegerField()
    tipo_servicio = models.ForeignKey('TipoServicio', on_delete=models.CASCADE)
    manicurista = models.ForeignKey('Manicurista', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id_servicio)

class Manicurista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rut = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    certifications = models.FileField(upload_to='certifications/', blank=True, null=True)
    state = models.BooleanField(default=False)
    motivo_rechazo = models.TextField(blank=True, null=True)
    certificado_actualizado = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

