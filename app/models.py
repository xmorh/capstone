from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class Cliente(models.Model):
#     id_cliente = models.AutoField(primary_key=True)
#     run_cliente = models.CharField(max_length=12)
#     nombre_cliente = models.CharField(max_length=100)
#     email_cliente = models.CharField(max_length=100)
#     password_cliente = models.CharField(max_length=8)
#     telefono_cliente = models.IntegerField()

#     def __str__(self):
#         return self.run_cliente


# class Manicurista(models.Model):
#     id_manicurista = models.AutoField(primary_key=True)
#     run_manicurista = models.CharField(max_length=12)
#     nombre_manicurista = models.CharField(max_length=100)
#     email_manicurista = models.CharField(max_length=100)
#     password_manicurista = models.CharField(max_length=8)
#     telefono_manicurista = models.IntegerField()
#     foto = models.CharField(max_length=100)
#     certificacion = models.CharField(max_length=100)

#     def __str__(self):
#         return self.run_manicurista

# class Reserva(models.Model):
#     id_reserva = models.AutoField(primary_key=True)
#     fecha_reserva = models.DateField()
#     hora_reserva = models.TimeField()
#     id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.id_reserva


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.IntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    
class Tipo_servicio(models.Model):
    id_tipo_servicio = models.AutoField(primary_key=True)
    nombre_tipo_servicio = models.CharField(max_length=50)
    duracion = models.IntegerField()

    def __str__(self):
        return self.id_tipo_servicio
    
class Manicurista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rut = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    certifications = models.FileField(upload_to='certifications/')



