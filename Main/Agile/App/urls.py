from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.logear, name='logear'),
    path('dashboard', views.home, name='dashboard'),
    path('salir', views.salir, name='salir'),
    path('ausuario', views.ausuario, name='ausuario'),
    path('musuario/<str:alias>', views.musuario, name='musuario'),
    path('busuario/<str:alias>/<str:aux>', views.busuario, name='busuario'),
    path('listar', views.listar, name='listar'),
]