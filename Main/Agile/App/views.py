from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from App.models import Usuario
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Sprint, Backlog, Comentario_Us, Usuario, Permiso, Rol, Usuario_Proyecto, Usuario_Rol, User_Story, Estado_Us, Proyecto, Estado_Proyecto, Rol_Permiso, Estado_Sprint
from datetime import datetime, date, timedelta

def validarPermisos(request, permiso):
    rolusuario = listar_usurol(request.user.id)
    result = False
    for rol in rolusuario:
        rolespermisos = buscar_rol_permisob(rol.id_rol)
        for permisos in rolespermisos:
            print(permisos.id_permiso)
            if permisos.id_permiso.nombre == permiso:
                result = True
    return result

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
    if not validarPermisos(request, 'LISTAR_USUARIO'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_USUARIO')
    modificar = validarPermisos(request, 'MODIFICAR_USUARIO')
    eliminar = validarPermisos(request, 'ELIMINAR_USUARIO')
    rol = validarPermisos(request, 'ROL_USUARIO')

    usuarios = Usuario.objects.all()
    return render(request, 'paginas/users.html', {'usuarios': usuarios, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar, 'rol': rol})

#Retorna todos los permisos de la base de datos
def permisos(request):
    if not validarPermisos(request, 'LISTAR_PERMISO'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_PERMISO')
    modificar = validarPermisos(request, 'MODIFICAR_PERMISO')
    eliminar = validarPermisos(request, 'ELIMINAR_PERMISO')
    

    permisos = Permiso.objects.all()
    return render(request, 'paginas/permisos.html', {'permisos': permisos, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar})
#Retorna todos los roles de la base de datos
def roles(request):

    if not validarPermisos(request, 'LISTAR_ROL'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_ROL')
    modificar = validarPermisos(request, 'MODIFICAR_ROL')
    eliminar = validarPermisos(request, 'ELIMINAR_ROL')

    roles = Rol.objects.all()
    return render(request, 'paginas/roles.html', {'roles': roles, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar})

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
    return render(request, 'usuarios/crear.html',{'roles': roles})

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
    return render(request,'usuarios/modificar.html',datos)

#Eliminar Usuario
def busuario(request, alias, aux):
    if aux == 'si':
        usu = buscar(alias)
        usu.delete()
        #messages.success(request,"Usuario eliminado exitosamente")
        return redirect('users')
    return render(request,'usuarios/eliminar.html',{'alias':alias})

#Asignar Rol a Usuario
def usurol(request,alias):
    usu = buscar(alias)
    usurol = listar_usurol(usu)
    if request.method == 'POST':
        if request.POST['roles'] != '0':
            rol_nombre = request.POST['roles']
            desde = datetime.date(datetime.strptime(request.POST['desde'],'%Y-%m-%d'))
            hasta = datetime.date(datetime.strptime(request.POST['hasta'],'%Y-%m-%d'))
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
    return render(request,'App/usurol.html',{'roles':roles,'alias':alias,'usurol':usurol})

def listar_usurol(usu):
    return Usuario_Rol.objects.filter(id_usuario=usu).all()

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

#Crear Rol
def crol(request):
    permisos = listar_permisos()
    if request.method == 'POST':
        nombre      = request.POST['nombre']
        descripcion = request.POST['descripcion']
        rol = Rol(nombre=nombre, descripcion=descripcion)
        rol.save()
        for id_permiso in request.POST.getlist('permiso'):
            permiso = buscar_permiso(id_permiso)
            if buscar_rol_permiso(rol,permiso) is None:
                rol_permiso = Rol_Permiso(id_rol=rol,id_permiso=permiso)
                rol_permiso.save()
        return redirect('roles') 
    return render(request,"App/crol.html",{'permisos':permisos})

def buscarrol(id):
    rol = Rol.objects.filter(id=id).first()
    return rol

def mrol(request, rol):
    permisos = listar_permisos()
    rol_edit= buscarrol(rol)
    permisos_rol = listar_permisos_rol(rol_edit)

    if request.method == 'POST':
        rol_edit.nombre      = request.POST['nombre']
        rol_edit.descripcion = request.POST['descripcion']
        rol_edit.save()
        eliminar_permisos(rol_edit)
        for id_permiso in request.POST.getlist('permiso'):
            permiso = buscar_permiso(id_permiso)
            if buscar_rol_permiso(rol_edit,permiso) is None:
                rol_permiso = Rol_Permiso(id_rol=rol_edit,id_permiso=permiso)
                rol_permiso.save()
        return redirect('roles')            
    return render(request,"App/mrol.html",{'rol':rol_edit,'permisos':permisos,'permisos_rol':permisos_rol})
    
def erol(request, rol, aux):
    roll = buscarrol(rol)
    if aux == 'si':        
        roll.delete()
        return redirect('roles')
    return render(request,'App/erol.html',{'rol':roll})

#Busca y retorna el usuario que recibe como parametro
def buscar(alias):
    users = Usuario.objects.filter(alias=alias).first()
    return users

#Busca y retorna permisos
def buscarP(nombre):
    permisos = Permiso.objects.filter(nombre=nombre).first()
    return permisos

#Crear User Story
def aus(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        #La fecha de cracion carga automaticamente la fecha actual
        fecha_creacion = datetime.today().strftime('%Y-%m-%d')
        us = User_Story(
            nombre = nombre,
            descripcion = descripcion,
            fecha_creacion = fecha_creacion
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
        messages.success(request,"User Story eliminado exitosamente")
        return redirect('us')
    return render(request,'App/bus.html',{'us':us})

#Listar y añadir US en Backlog
def backlog(request,id_proyecto):
    user_story = listar_us()
    proyecto = buscar_proyecto(id_proyecto)
    us_backlog = listar_us_backlog(proyecto)
    if request.method == 'POST':
        if request.POST['us'] != '0':
            us = buscar_us(request.POST['us'])
            if buscar_us_backlog(us,proyecto) is None:
                backlog = Backlog(id_proyecto=proyecto,id_us=us)
                backlog.save()
                messages.success(request,'User Story añadido')
            else:
                messages.error(request,'El User Story ya esta añadido')
        else:
            messages.error(request,'Seleccione un User Story')
    return render(request,'App/backlog.html',{'user_story':user_story,'us_backlog':us_backlog,'proyecto':proyecto})

#Eliminar US de Backlog
def eus(request,id_proyecto,id_us,aux):
    proyecto = buscar_proyecto(id_proyecto)
    us = buscar_us(id_us)
    if aux == 'si':
        us_backlog = buscar_us_backlog(us,proyecto)
        us_backlog.delete()
        messages.success(request,'User Story removido')
        return redirect('backlog',id_proyecto)
    return render(request,'App/eus.html',{'proyecto':proyecto,'us':us})

#Verifica si un US esta asociado a un Backlog
def buscar_us_backlog(us,proyecto):
    return Backlog.objects.filter(id_us=us,id_proyecto=proyecto).first()

def buscar_us(id_us):
    return User_Story.objects.filter(id=id_us).first()
#Retorna los User Story de un backlog
def listar_us_backlog(proyecto):
    return Backlog.objects.filter(id_proyecto=proyecto).all()

#Busca un Proyecto dado un ID
def buscar_proyecto(id_proyecto):
    return Proyecto.objects.filter(id = id_proyecto).first()

#Obtener permisos
def listar_permisos():
    return Permiso.objects.all()

#Retorna el permiso con el id que recibe
def buscar_permiso(id_permiso):
    return Permiso.objects.filter(id=id_permiso).first()

#Retorna los Rermisos que tiene el Rol que recibe
def listar_permisos_rol(id_rol):
    aux = Rol_Permiso.objects.filter(id_rol=id_rol)
    perm = set()
    for x in aux:
        perm.add(x.perm())
    return perm

#Retorna el Rol y el Permiso si tiene asignado
def buscar_rol_permisob(id_rol):
    return Rol_Permiso.objects.filter(id_rol = id_rol).all()

#Retorna el Rol y el Permiso si tiene asignado
def buscar_rol_permiso(id_rol,permiso):
    return Rol_Permiso.objects.filter(id_rol = id_rol, id_permiso = permiso).first()

#Retorna todos los Proyectos de la base de datos
def listar_proyectos():
    return Proyecto.objects.all()

#Elimina todos los permisos de un rol
def eliminar_permisos(rol_edit):
    aux = Rol_Permiso.objects.filter(id_rol=rol_edit).all()
    for a in aux:
        a.delete()
#Retorna todos los proyectos de la base de datos
def proyectos(request):

    if not validarPermisos(request, 'LISTAR_PROYECTO'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_PROYECTO')
    modificar = validarPermisos(request, 'MODIFICAR_PROYECTO')
    eliminar = validarPermisos(request, 'ELIMINAR_PROYECTO')

    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/index.html', {'proyectos': proyectos, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar})

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

#Eliminar proyecto
def eproy(request, nombre, aux):
    if aux == 'si':
        proy = buscarproy(nombre)
        proy.delete()
        #messages.success(request,"Proyecto eliminado exitosamente")
        return redirect('proyectos')
    return render(request,'proyectos/eliminar.html',{'nombre':nombre})

def backlogs(request):

    if not validarPermisos(request, 'LISTAR_BACKLOG'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_BACKLOG')
    modificar = validarPermisos(request, 'MODIFICAR_BACKLOG')
    eliminar = validarPermisos(request, 'ELIMINAR_BACKLOG')
    
    backlogs = Backlog.objects.values('id_proyecto').distinct()
    proyectos = []
    for b in backlogs:
        proyectos.append(buscar_proyecto(b['id_proyecto']))
    
    return render(request,'paginas/backlogs.html',{'proyectos':proyectos, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar})

def sprint_activo(id_proyecto):
    estado = Estado_Sprint.objects.filter(id=2).first()
    proyecto = buscar_proyecto(id_proyecto)
    return Sprint.objects.filter(id_proyecto = proyecto, id_estado_sprint = estado).first()

def listar_us_sprint_activo(id_proyecto):
    sprint = sprint_activo(id_proyecto)
    return Backlog.objects.filter(id_sprint = sprint).all()

def kanban(request):

    if not validarPermisos(request, 'LISTAR_KANBAN'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_KANBAN')
    modificar = validarPermisos(request, 'MODIFICAR_KANBAN')
    eliminar = validarPermisos(request, 'ELIMINAR_KANBAN')
    mover_us = validarPermisos(request, 'MOVER_US_KANBAN')
    
    user_story = listar_us()
    usuarios = Usuario.objects.all()

    context = {
        'user_story' : user_story,
        'usuarios' : usuarios,
        'nuevo': nuevo,
        'modificar': modificar,
        'eliminar': eliminar,
        'mover_us': mover_us,
    }

    if request.method == 'POST':
        sprint = sprint_activo(id_proyecto)
        us = buscar_us(request.POST['id_us'])
        us_backlog = Backlog.objects.filter(id_sprint = sprint, id_us = us).first()
        if request.POST['estado'] == '1':
            if request.POST['usuario'] != '0':               
               usuario = Usuario.objects.filter(id = request.POST['usuario']).first()
               estado = Estado_Us.objects.filter(id=2).first()
               us_backlog.id_usuario = usuario
            else:
                messages.error(request,'Debe asignar un usuario')
                return redirect('kanban',id_proyecto)
        elif request.POST['estado'] == '2':
            if us_backlog.id_usuario == request.user:
                estado = Estado_Us.objects.filter(id=3).first()
            else:
                messages.error(request,'No puede mover el US')
                return redirect('kanban', id_proyecto)
        us_backlog.id_estado = estado
        us_backlog.save()
        if request.POST['comentario'] != '':
            comentario = Comentario_Us(comentario=request.POST['comentario'],id_usuario=request.user,id_user_story=us)
            comentario.save()
    return render(request,'App/kanban.html',context=context)

def integrantes_proyecto(id_proyecto):
    proyecto = buscar_proyecto(id_proyecto)
    return Usuario_Proyecto.objects.filter(id_proyecto=proyecto).all()

def buscar_integrante(id_proyecto,id_usuario):
    return Usuario_Proyecto.objects.filter(id_proyecto=id_proyecto,id_usuario=id_usuario).first()

def proyecto(request,id):
    proyecto = buscar_proyecto(id)
    integrantes = integrantes_proyecto(id)
    backlog = listar_us_backlog(id)
    sprints = Sprint.objects.filter(id_proyecto=proyecto)
    context = {
        'proyecto' : proyecto,
        'integrantes' : integrantes,
        'backlog' : backlog,
        'sprints' : sprints,
    }
    return render(request,'proyectos/proyecto.html',context=context)

def miembro(request,id):
    usuarios = Usuario.objects.all()
    miembros = integrantes_proyecto(id)
    proyecto = buscar_proyecto(id)
    context = {
        'proyecto' : proyecto,
        'usuarios' : usuarios,
        'miembros' : miembros,
    }
    if request.method == 'POST':
        if request.POST['integrante'] != '0':
            usuario = Usuario.objects.filter(id=request.POST['integrante']).first()
            if buscar_integrante(id_usuario=usuario,id_proyecto=proyecto) is None:
                integrante = Usuario_Proyecto(id_proyecto=proyecto,id_usuario=usuario)
                integrante.save()
                messages.success(request,'Usuario agregado')
            else:
                messages.error(request,'El usuario ya es miebro')
        else:   
            messages.error(request,'Selecciones un usuario')
    return render(request,'proyectos/integrantes.html',context=context)

def bmiembro(request,id_proyecto,id_usuario):
    integrante = buscar_integrante(id_proyecto=id_proyecto,id_usuario=id_usuario)
    integrante.delete()
    messages.success(request,'Miembro eliminado')
    return redirect('miembro',id_proyecto)

def userstory(request,id_us):

    if not validarPermisos(request, 'LISTAR_USER_STORY'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_USER_STORY')
    modificar = validarPermisos(request, 'MODIFICAR_USER_STORY')
    eliminar = validarPermisos(request, 'ELIMINAR_USER_STORY')

    us = buscar_us(id_us)
    comentarios = Comentario_Us.objects.filter(id_user_story=id_us).all()
    context = {
        'us' : us,
        'comentarios' : comentarios,
        'nuevo': nuevo,
        'modificar': modificar,
        'eliminar': eliminar,
    }
    return render(request,'App/userstory.html',context=context)
        
#Crear SPRINT
def asprint(request):
    proyectos = listar_proyectos()
    context = {
        'proyectos' : proyectos
    }
    if request.method == 'POST':
        if request.POST['proyecto'] != '0':
            descripcion = request.POST['descripcion']
            fecha_inicio = datetime.date(datetime.strptime(request.POST['fecha_inicio'],'%Y-%m-%d'))

            if request.POST['duracion']=="":
                duracion = 14
            else:
                duracion = int(request.POST['duracion'])

            sprint = Sprint(
                id_proyecto = buscar_proyecto(request.POST['proyecto']),
                descripcion=descripcion, 
                duracion=duracion,
                fecha_inicio=fecha_inicio, 
                fecha_fin=fecha_inicio + timedelta(days=duracion),
                )

            # verifica el estado del sprint
            hoy = datetime.now().date()
            if hoy >= fecha_inicio and hoy <= fecha_fin:
                estado = Estado_Sprint.objects.filter(id=2).first()  # Doing
                sprint.id_estado_sprint = estado
            elif fecha_inicio < hoy and fecha_fin < hoy:
                estado = Estado_Sprint.objects.filter(id=3).first()  # Done
                sprint.id_estado_sprint = estado
            else:
                estado = Estado_Sprint.objects.filter(id=1).first()  # To do
                sprint.id_estado_sprint = estado

            sprint.save()
        else:
            messages.error(request,'Seleccione un proyecto')
            return redirect('asprint')
        return redirect('sprints',id_proyecto=0) 
    return render(request,"App/asprint.html",context=context)
    
#Lista los sprints existentes
def sprints(request,id_proyecto):

    if not validarPermisos(request, 'LISTAR_SPRINT'):
        return redirect('home')
    
    nuevo = validarPermisos(request, 'NUEVO_SPRINT')
    modificar = validarPermisos(request, 'MODIFICAR_SPRINT')
    eliminar = validarPermisos(request, 'ELIMINAR_SPRINT')
    iniciar = validarPermisos(request, 'INICIAR_SPRINT')
    backlog = validarPermisos(request, 'BACKLOG_SPRINT')

    if id_proyecto != 0:
        proyecto = buscar_proyecto(id_proyecto)
        sprint = Sprint.objects.filter(id_proyecto=proyecto).all()
    else:
        sprint = Sprint.objects.all()
    return render(request, 'App/sprints.html', {'sprint': sprint, 'nuevo': nuevo, 'modificar': modificar, 'eliminar': eliminar, 'iniciar': iniciar, 'backlog': backlog})

def bsprint(spr):
    id = Sprint.objects.filter(id=spr).first()
    return id

def msprint(request, spr):
    sprint_edit= bsprint(spr)
    datos={
        'descripcion':sprint_edit.descripcion,
        'fecha_inicio':sprint_edit.fecha_inicio,
        'duracion':sprint_edit.duracion,
    }
    if request.method == 'POST':
        sprint_edit.descripcion = request.POST['descripcion']
        sprint_edit.fecha_inicio = datetime.date(datetime.strptime(request.POST['fecha_inicio'],'%Y-%m-%d'))
        
        if request.POST['duracion']=="":
            duracion = 14
        else:
            duracion = int(request.POST['duracion'])
        sprint_edit.fecha_fin = sprint_edit.fecha_inicio + timedelta(days=duracion)

        # verifica el estado del sprint
        hoy = datetime.now().date()
        if hoy >= sprint_edit.fecha_inicio and hoy <= sprint_edit.fecha_fin:
            estado = Estado_Sprint.objects.filter(id=2).first()  # Doing
            sprint_edit.id_estado_sprint = estado
        elif sprint_edit.fecha_inicio < hoy and sprint_edit.fecha_fin < hoy:
            estado = Estado_Sprint.objects.filter(id=3).first()  # Done
            sprint_edit.id_estado_sprint = estado
        else:
            estado = Estado_Sprint.objects.filter(id=1).first()  # To do
            sprint_edit.id_estado_sprint = estado
         
        sprint_edit.save()
        return redirect('sprints', id_proyecto = 0)           
    return render(request,"app/msprint.html",datos)

#Lista y permite añadir US a un Sprint
def sprint(request,id_sprint):
    sprint = Sprint.objects.filter(id = id_sprint).first()
    user_story = Backlog.objects.filter(id_proyecto = sprint.id_proyecto, id_sprint__isnull = True).all()
    backlog = Backlog.objects.filter(id_proyecto = sprint.id_proyecto, id_sprint = sprint).all()
    context = {
        'user_story' : user_story,
        'backlog' : backlog
    }
    if request.method == 'POST':
        if request.POST['us'] != '0':
            to_do = Estado_Sprint.objects.filter(id = 1).first()
            if sprint.id_estado_sprint == to_do:
                us = User_Story.objects.filter(id = request.POST['us']).first()
                us_backlog = Backlog.objects.filter(id_proyecto = sprint.id_proyecto, id_us = us).first()
                us_backlog.id_sprint = sprint
                us_backlog.prioridad = request.POST['prioridad']
                us_backlog.save()
                messages.success(request,'US añadido')
            else:
                messages.error(request,"Sprint en curso o finalizado.")    
        else:
            messages.error(request,'Seleccione un US') 
        return redirect('sprint',id_sprint)            
    return render(request,'App/sprint.html', context=context)

def esprint(request,id_backlog):
    us = Backlog.objects.filter(id = id_backlog).first()
    aux = us.id_sprint.id   
    to_do = Estado_Sprint.objects.filter(id = 1).first()
    if us.id_sprint.id_estado_sprint == to_do:
        us.id_sprint = None
        us.save()
        messages.success(request,'US eliminado')
    else:
        messages.error(request,"Sprint en curso o finalizado.") 
    return redirect('sprint',aux)
    
def burndown(request, id_proyecto):
    proyecto = buscar_proyecto(id_proyecto)
    sprints = Sprint.objects.filter(id_proyecto = proyecto).all().order_by("fecha_inicio")
    us_finalizados = [Backlog.objects.filter(id_proyecto = proyecto).all().count()]
    done = Estado_Us.objects.filter(id = 3).first()
    for sprint in sprints:
        aux = us_finalizados[-1] - Backlog.objects.filter(id_sprint = sprint, id_estado = done).all().count()
        us_finalizados.append(aux)
    context = {
        'proyecto' : proyecto,
        'sprints' : sprints,
        'us_finalizados' : us_finalizados,
    }
    return render(request,'App/burndown.html', context=context)

#Crear Permiso
def apermiso(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']        
        descripcion = request.POST['descripcion']        
        if Permiso.objects.filter(nombre=nombre):
            messages.error(request,'El permiso "' + nombre + '" ya existe')
            return redirect('apermiso')
        else:
            permiso = Permiso(nombre=nombre, descripcion=descripcion)
            permiso.save()
            return redirect('permisos')
    return render(request, 'paginas/apermiso.html')


#Modificar Permiso
def mpermiso(request,nombre):
    if not validarPermisos(request, 'MODIFICAR_PERMISO'):
        return redirect('home')
    perm = buscarP(nombre)
    datos = {
        'nombre': perm.nombre,
        'descripcion':perm.descripcion,
    }
    if request.method == 'POST':
        cambio = False
        #Verifica si se modifico algun campo del permiso
        if request.POST['nombre'] != perm.nombre:
            perm.nombre = request.POST['nombre']
            cambio = True
        if request.POST['descripcion'] != perm.descripcion:
            perm.descripcion = request.POST['descripcion']
            cambio = True
        #Su hubo cambios, los guarda en la base de datos
        if cambio:
            perm.save()
            messages.success(request,'Modificacion exitosa')
            return redirect('permisos')
        #Sino vuelve a Consultar
        else:
            #messages.error(request,'No se realizo ningun cambio')
            return redirect('permisos')
    return render(request,'paginas/mpermiso.html',datos)

#Eliminar Usuario
def bpermiso(request, nombre, aux):
    if aux == 'si':
        perm = buscarP(nombre)
        perm.delete()
        return redirect('permisos')
    return render(request,'paginas/bpermiso.html',{'nombre':nombre})

#Iniciar Sprint
def iniciar_sprint(request, spr):
    sprint = bsprint(spr)
    datos={
        'descripcion':sprint.descripcion,
        'duracion':sprint.duracion,
    }
    if request.method == 'POST':
        sprint.descripcion = request.POST['descripcion']
        sprint.fecha_inicio = datetime.now().date()

        if request.POST['duracion']=="":
            duracion = 14
        else:
            duracion = int(request.POST['duracion'])
        sprint.fecha_fin = sprint.fecha_inicio + timedelta(days=duracion)

        estado = Estado_Sprint.objects.filter(id=2).first()  # Doing
        sprint.id_estado_sprint = estado
        sprint.save()
        return redirect('sprints', id_proyecto=0)
    return render(request,"app/isprint.html",datos)
