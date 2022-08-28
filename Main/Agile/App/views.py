from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from App.models import Usuario
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

#Retorna todos los usuarios de la base de datos
def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'paginas/users.html', {'usuarios': usuarios})
#Retorna todos los permisos de la base de datos
def permisos(request):
    permisos = Permiso.objects.all()
    return render(request, 'paginas/permisos.html', {'permisos': permisos})
#Retorna todos los roles de la base de datos
def roles(request):
    roles = Rol.objects.all()
    return render(request, 'paginas/roles.html', {'roles': roles})

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
            return redirect('users')
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
            return redirect('users')
        #Sino vuelve a Consultar
        else:
            messages.error(request,'No se realizo ningun cambio')
            return redirect('users')
    return render(request,'App/musuario.html',datos)

def busuario(request, alias, aux):
    if aux == 'si':
        usu = buscar(alias)
        usu.delete()
        messages.success(request,"Usuario eliminado exitosamente")
        return redirect('users')
    return render(request,'App/busuario.html',{'alias':alias})

#Retorna todos los usarios de la base de datos
def listar(request):
    users = Usuario.objects.all()
    return render(request,'App/a.html',{'users':users})
def crol(request):
    if request.method == 'POST':
        nombre      = request.POST['nombre']
        descripcion = request.POST['descripcion']
        rol = Rol(nombre=nombre, descripcion=descripcion)
        rol.save()
        return redirect('roles') 
    return render(request,"App/crol.html")

def buscarrol(nombre):
    rol = Rol.objects.filter(nombre=nombre).first()
    return rol

def mrol(request, rol):

    rol_edit= buscarrol(rol)
    datos={
        'nombre':rol_edit.nombre,
        'descripcion':rol_edit.descripcion,
    }
    
    if request.method == 'POST':
        rol_edit.nombre      = request.POST['nombre']
        rol_edit.descripcion = request.POST['descripcion']
        rol_edit.save()
        return redirect('roles')            
    return render(request,"App/mrol.html",datos)
    
def erol(request, rol, aux):
    if aux == 'si':
        roll = buscarrol(rol)
        roll.delete()
        return redirect('roles')
    return render(request,'App/erol.html',{'rol':rol})
    
def listarol(request):
    rolex = Rol.objects.all()
    return render(request,'App/arol.html',{'rolex':rolex})

#Busca y retorna el usuario que recibe como parametro
def buscar(alias):
    users = Usuario.objects.filter(alias=alias).first()
    return users
