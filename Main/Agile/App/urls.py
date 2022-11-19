from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('', views.logear, name='logear'),
    path('dashboard', views.home, name='dashboard'),
    path('users', views.usuarios, name='users'),
    path('permisos', views.permisos, name='permisos'),
    path('roles', views.roles, name='roles'),
    path('salir', views.salir, name='salir'),
    path('ausuario', views.ausuario, name='ausuario'),
    path('musuario/<str:alias>', views.musuario, name='musuario'),
    path('busuario/<str:alias>/<str:aux>', views.busuario, name='busuario'),
    path('crol', views.crol, name='crol'),
    path('mrol/<str:rol>', views.mrol, name='mrol'),
    path('erol/<str:rol>/<str:aux>', views.erol, name='erol'),
    path('usurol/<str:alias>', views.usurol, name='usurol'),
    path('us', views.us, name='us'),
    path('aus', views.aus, name='aus'),
    path('mus/<int:id_us>', views.mus, name='mus'),
    path('bus/<int:id_us>/<str:aux>', views.bus, name='bus'),
    path('proyectos', views.proyectos, name='proyectos'),
    path('aproyecto', views.aproyecto, name='aproyecto'),
    path('sprints/<int:id_proyecto>', views.sprints, name='sprints'),
    path('sprint/<int:id_sprint>', views.sprint, name='sprint'),
    path('esprint/<int:id_backlog>', views.esprint, name='esprint'),
    path('asprint', views.asprint, name='asprint'),
    path('msprint/<int:spr>', views.msprint, name='msprint'),
    path('mproy/<str:proyecto>', views.mproy, name='mproy'),
    path('eproy/<str:nombre>/<str:aux>', views.eproy, name='eproy'),
    path('backlog/<int:id_proyecto>', views.backlog, name='backlog'),
    path('backlogs', views.backlogs, name='backlogs'),
    path('eus/<int:id_proyecto>/<int:id_us>/<str:aux>', views.eus, name='eus'),
    path('kanban', views.kanban, name='kanban'),
    path('proyecto/<int:id>', views.proyecto, name='proyecto'),
    path('miembro/<int:id>', views.miembro, name='miembro'),
    path('bmiembro/<int:id_proyecto>/<int:id_usuario>', views.bmiembro, name='bmiembro'),
    path('userstory/<int:id_us>', views.userstory, name='userstory'),
    path('permisos', views.permisos, name='permisos'),
    path('apermiso', views.apermiso, name='apermiso'),
    path('mpermiso/<str:nombre>', views.mpermiso, name='mpermiso'),
    path('bpermiso/<str:nombre>/<str:aux>', views.bpermiso, name='bpermiso'),
]