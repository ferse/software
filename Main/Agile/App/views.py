from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Usuario, Permiso, Rol

# Create your views here.
def home(request):
    #Redirecciona al login si no inicio sesion y trata de entrar desde la URL
    if not request.user.is_authenticated:
        return redirect('logear')
    return render(request,"App/index.html")

def logear(request):
    #Si ya esta logeado redirecciona al inicio
    if request.user.is_authenticated:
        return redirect('home')
    #Recibe los datos del formulario y almacena en las variables
    if request.method == 'POST':
        alias = request.POST['usuario']
        contra = request.POST['password']
        #print(alias,contra)
        user = authenticate(request,username=alias, password=contra)
        #print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario no valido")
            print("No valido")
            return redirect('logear')
    return render(request,"App/login.html")

def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'paginas/users.html', {'usuarios': usuarios})

def permisos(request):
    permisos = Permiso.objects.all()
    return render(request, 'paginas/permisos.html', {'permisos': permisos})

def roles(request):
    roles = Rol.objects.all()
    return render(request, 'paginas/roles.html', {'roles': roles})

def salir(request):
    logout(request)
    return redirect('logear')