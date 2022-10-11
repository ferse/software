from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, email, alias, nombre, apellido, password=None):
        if not email:
            raise ValueError("Insertar email")
        if not alias:
            raise ValueError("Insertar alias")
        if not nombre:
            raise ValueError("Insertar nombre")
        if not apellido:
            raise ValueError("Insertar apellido")
        usuario = self.model(
			email=self.normalize_email(email),
			alias = alias,
            nombre = nombre,
            apellido = apellido
		)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, alias, nombre, apellido, password=None):
        usuario = self.create_user(
			email = self.normalize_email(email),
            nombre = nombre,
            apellido = apellido,
			password = password,
			alias = alias
		)
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser):
    alias = models.CharField(unique=True, max_length=20, verbose_name='alias')
    email = models.EmailField(max_length=60, verbose_name='email')
    nombre = models.CharField(max_length=20, verbose_name='nombre')
    apellido = models.CharField(max_length=20, verbose_name='apellido')
    date_joined	= models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'alias'
    REQUIRED_FIELDS = ['email','nombre','apellido']

    objects = MyAccountManager()

    def __str__(self):
        f1_str = self.date_joined.strftime("%d/%m/%Y")
        f2_str = self.last_login.strftime("%d/%m/%Y")

        fila = "Alias: " + self.alias + " - " + "Email: " + self.email + " - " + "Nombre: " + self.nombre + " - " + "Apellido: " + self.apellido + " - " + "Joined: " + f1_str + " - " + "Last Login: " + f2_str + " - " + "Admin: " + str(self.is_admin) + " - " + "Activo: " + str(self.is_active)
        return fila

    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
	    return self.is_admin

class Formulario(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='nombre')

class Permiso(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='nombre')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    
    def __str__(self):
        fila = "ID: " + str(self.id_formulario) + " - " + "Nombre: " + self.nombre + " - " + "Descripcion: " + self.descripcion
        return fila

class Rol(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='nombre')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')

    def __str__(self):
        fila = "Nombre: " + self.nombre + " - " + "Descripcion: " + self.descripcion
        return fila

class Rol_Permiso(models.Model):
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    id_permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    def perm(self):
        return self.id_permiso.id

class Usuario_Rol(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_desde = models.DateField()
    fecha_hasta = models.DateField()

class Estado_Proyecto(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')

class Estado_Us(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')

class Proyecto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='nombre')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_estado = models.ForeignKey(Estado_Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        fila = "Proyecto: " + self.nombre + " - " + "Descripcion: " + self.descripcion + " - " + "Fecha inicio: " + self.fecha_inicio + " - " + "Fecha fin: " + self.fecha_fin 
        return fila

class Usuario_Proyecto(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Sprint(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')
    duracion = models.IntegerField(verbose_name='duracion')
    fecha_inicio = models.DateField(verbose_name='Fecha Inicio')
    fecha_fin = models.DateField(verbose_name='Fecha Fin')
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

class User_Story(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='nombre')
    descripcion = models.CharField(max_length=100, verbose_name='descripcion')
    fecha_creacion = models.DateField()
    prioridad = models.IntegerField(verbose_name='Prioridad')
    id_sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    id_estado = models.ForeignKey(Estado_Us, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)

class Comentario_Us(models.Model):
    comentario = models.TextField(verbose_name='Comentario')
    id_user_story = models.ForeignKey(User_Story, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)

class Backlog(models.Model):
    id_proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    id_sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    id_us = models.ForeignKey(User_Story, on_delete=models.CASCADE)