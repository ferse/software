from subprocess import ABOVE_NORMAL_PRIORITY_CLASS
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from App.models import Usuario
from django.conf import settings
from .models import Usuario, Permiso, Rol, Usuario_Rol, User_Story, Estado_Us, Proyecto, Estado_Proyecto
from datetime import datetime, date

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

#Crear Usuario
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
    roles = Rol.objects.all() 
    return render(request, 'App/ausuario.html',{'roles': roles})

#Modificar Usuario
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
        if request.POST['alias'] != usu.alias:
            usu.alias = request.POST['alias']
            cambio = True
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
                return redirect('musuario',alias=alias)
        #Su hubo cambios, los guarda en la base de datos
        if cambio:
            usu.save()
            messages.success(request,'Modificacion exitosa')
            return redirect('users')
        #Sino vuelve a Consultar
        else:
            #messages.error(request,'No se realizo ningun cambio')
            return redirect('users')
    return render(request,'App/musuario.html',datos)

#Eliminar Usuario
def busuario(request, alias, aux):
    if aux == 'si':
        usu = buscar(alias)
        usu.delete()
        #messages.success(request,"Usuario eliminado exitosamente")
        return redirect('users')
    return render(request,'App/busuario.html',{'alias':alias})

#Asignar Rol a Usuario
def usurol(request,alias):
    if request.method == 'POST':
        #print(request.POST['roles'])  
        if request.POST['roles'] != '0':
            rol_nombre = request.POST['roles']
            usu = buscar(alias)
            desde = datetime.date(datetime.strptime(request.POST['desde'],'%Y-%m-%d'))
            hasta = datetime.date(datetime.strptime(request.POST['hasta'],'%Y-%m-%d'))
            #print(comprobar_fecha(usu, desde, hasta))
            if hasta <= desde:
                messages.error(request,'Fecha Hasta debe ser mayor a fecha Desde')
                return redirect('usurol',alias=alias)
            if comprobar_fecha(usu,desde,hasta):
                rol = buscarrol(rol_nombre)
                usu_rol = Usuario_Rol(id_usuario=usu, id_rol=rol, fecha_desde=desde, fecha_hasta=hasta)
                usu_rol.save()
                return redirect('users')
            else:
                messages.error(request,'El usuario ya tiene rol durante esas fechas')
                return redirect('usurol',alias=alias)
    roles = Rol.objects.all()
    return render(request,'App/usurol.html',{'roles':roles,'alias':alias})

#Comprueba que un usuario no tenga 2 roles en la misma fecha
def comprobar_fecha(usu, desde, hasta):
    roles = Usuario_Rol.objects.filter(id_usuario=usu)
    for rol in roles:
        #Si la fecha de inicio coincide con otro rol retorna Falso
        if rol.fecha_desde <= desde <= rol.fecha_hasta:
            return False
        #Si la fecha de fin coincide con otro rol retorna Falso
        if rol.fecha_desde <= hasta <= rol.fecha_hasta:
            return False
    #Si las fecha no coinciden con otro rol retorna True
    return True

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

#Crear User Story
def aus(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        #La fecha de cracion carga automaticamente la fecha actual
        fecha_creacion = datetime.today().strftime('%Y-%m-%d')
        #Estado por defecto es TO DO
        estado = Estado_Us.objects.filter(descripcion='To Do').first()
        us = User_Story(
            nombre = nombre,
            descripcion = descripcion,
            fecha_creacion = fecha_creacion,
            #Prioridad por defecto es 0
            prioridad = 0,
            id_estado = estado
            )
        us.save()
        messages.success(request,'User Story creado exitosamente')
        return redirect('us')
    return render(request,'App/aus.html')

#Modificar User Story
def mus(request,id_us):
    us = buscar_us(id_us)
    if request.method == 'POST':
        cambio = False
        if request.POST['nombre'] != us.nombre:
            us.nombre = request.POST['nombre']
            cambio = True
        if request.POST['descripcion'] != us.descripcion:
            us.descripcion = request.POST['descripcion']
            cambio = True
        if cambio:
            us.save()
            messages.success(request,'Modificacion exitosa')
            return redirect('us')
        #Sino vuelve a Consultar
        else:
            messages.error(request,'No se realizo ningun cambio')
            return redirect('us')
    return render(request,'App/mus.html',{'us':us})

#Pagina para listar User Story
def us(request):
    us = listar_us
    return render(request,'paginas/us.html',{'us':us})

#Retorna todos los User Story de la base de datos
def listar_us():
    return User_Story.objects.all()

#Retorna el User Story asociado al id que recibe
def buscar_us(id_us):
    return User_Story.objects.filter(id=id_us).first()

#Eliminar/Baja User Story
def bus(request, id_us, aux):
    us = buscar_us(id_us)
    if aux == 'si':
        us.delete()
        messages.success(request,"Usuario eliminado exitosamente")
        return redirect('us')
    return render(request,'App/bus.html',{'us':us})

#Retorna todos los proyectos de la base de datos
def proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/index.html', {'proyectos': proyectos})

#Crear Proyecto
def aproyecto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fecha_inicio = datetime.date(datetime.strptime(request.POST['fecha_inicio'],'%Y-%m-%d'))
        fecha_fin = datetime.date(datetime.strptime(request.POST['fecha_fin'],'%Y-%m-%d'))
        #Estado por defecto es TO DO
        estado = Estado_Proyecto.objects.filter(descripcion='To Do').first()
        #usuario = request.POST['usuario']     
        if fecha_fin <= fecha_inicio:
            messages.error(request,'Fecha fin debe ser mayor a fecha de inicio')
            return redirect('proyectos')
        proy = Proyecto(
            nombre=nombre, 
            descripcion=descripcion, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin,
            id_estado = estado
            #id_usuario_rol = usuario    # falta agregar usuario a un proyecto
            )
        proy.save()
        return redirect('proyectos') 
    return render(request,"proyectos/crear.html")

def buscarproy(nombre):
    proy = Proyecto.objects.filter(nombre=nombre).first()
    return proy

# Modificar proyectos
def mproy(request, proyecto):
    proy_edit= buscarproy(proyecto)
    datos={
        'nombre':proy_edit.nombre,
        'descripcion':proy_edit.descripcion,
        'fecha_inicio':proy_edit.fecha_inicio,
        'fecha_fin':proy_edit.fecha_fin,
    }
    if request.method == 'POST':
        proy_edit.nombre = request.POST['nombre']
        proy_edit.descripcion = request.POST['descripcion']
        proy_edit.fecha_inicio = datetime.date(datetime.strptime(request.POST['fecha_inicio'],'%Y-%m-%d'))
        proy_edit.fecha_fin = datetime.date(datetime.strptime(request.POST['fecha_fin'],'%Y-%m-%d'))       
        proy_edit.save()
        return redirect('proyectos')           
    return render(request,"proyectos/editar.html",datos)
