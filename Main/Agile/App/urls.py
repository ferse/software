from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
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
    path('listarol', views.listarol, name='listarol'),
    path('usurol/<str:alias>', views.usurol, name='usurol'),
    path('us', views.us, name='us'),
    path('aus', views.aus, name='aus'),
    path('mus/<int:id_us>', views.mus, name='mus'),
    path('bus/<int:id_us>/<str:aux>', views.bus, name='bus'),
    path('proyectos', views.proyectos, name='proyectos'),
    path('aproyecto', views.aproyecto, name='aproyecto'),
    path('mproy/<str:proyecto>', views.mproy, name='mproy'),
]