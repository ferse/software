from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from App.models import Usuario
from django.conf import settings

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
        alias = request.POST['alias']
        password = request.POST['contra']
        print(alias,password)
        user = authenticate(alias=alias, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario no valido")
            print("No valido")
            return redirect('logear')
    return render(request,"App/login.html")

def salir(request):
    logout(request)
    return redirect('logear')

def ausuario(request):
    if request.method == 'POST':
        alias = request.POST['alias']
        nombre = request.POST['nombre']        
        apellido = request.POST['apellido']        
        email = request.POST['email']
        contra1 = request.POST['contra1']
        contra2 = request.POST['contra2']
        if Usuario.objects.filter(alias=alias):
            messages.error(request,'El usuario "' + alias + '" ya existe')
            return redirect('ausuario')
        #print(alias)
        #print(nombre)
        #print(apellido)
        #print(email)
        #print(contra1)
        #print(contra2)
        if contra1 == contra2:
            usu = Usuario.objects.create_user(email, alias, nombre, apellido)
            usu.set_password(contra1)
            usu.save()
            messages.success(request,'Usuario creado exitosamente')
            return redirect('listar')
        else:
            messages.error(request,'Las contraseñas no coinciden')
            return redirect('ausuario')   
    return render(request, 'App/ausuario.html')

def musuario(request,alias):
    usu = buscar(alias)
    datos = {
        'alias': usu.alias,
        'nombre': usu.nombre,
        'apellido':usu.apellido,
        'email':usu.email,
    }
    if request.method == 'POST':
        cambio = False
        #Verifica si se modifico algun campo del formulario
        if request.POST['nombre'] != usu.nombre:
            usu.nombre = request.POST['nombre']
            cambio = True
        if request.POST['apellido'] != usu.apellido:
            usu.apellido = request.POST['apellido']
            cambio = True
        if request.POST['email'] != usu.email:
            usu.email = request.POST['email']
            cambio = True
        #Verifica si las contraseñas coinciden
        if request.POST['contra1'] != "":
            if request.POST['contra1'] == request.POST['contra2']:
                usu.set_password(request.POST['contra1'])
                cambio = True
            else:
                messages.error(request,'Las contraseñas no coinciden')
                return redirect('musuario')
        #Su hubo cambios, los guarda en la base de datos
        if cambio:
            usu.save()
            messages.success(request,'Modificacion exitosa')
            return redirect('listar')
        #Sino vuelve a Consultar
        else:
            messages.error(request,'No se realizo ningun cambio')
            return redirect('listar')
    return render(request,'App/musuario.html',datos)

def busuario(request, alias, aux):
    if aux == 'si':
        usu = buscar(alias)
        usu.delete()
        messages.success(request,"Usuario eliminado exitosamente")
        return redirect('listar')
    return render(request,'App/busuario.html',{'alias':alias})

#Retorna todos los usarios de la base de datos
def listar(request):
    users = Usuario.objects.all()
    return render(request,'App/a.html',{'users':users})

#Busca y retorna el usuario que recibe como parametro
def buscar(alias):
    users = Usuario.objects.filter(alias=alias).first()
    return users