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
        return self.alias
    def has_module_perms(self, app_label):
        return True
    def has_perm(self, perm, obj=None):
	    return self.is_admin