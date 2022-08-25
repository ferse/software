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
]