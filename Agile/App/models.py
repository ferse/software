from django.db import models

# Create your models here.
class Permisos(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)    
    descripcion = models.CharField(max_length=20)

class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)    
    descripcion = models.CharField(max_length=20)

class Usuario_Rol(models.Model):
    id_rol = 
    id_usuario =