from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
        alias = request.POST['usuario']
        contra = request.POST['password']
        #print(alias,contra)
        user = authenticate(username=alias, password=contra)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuario o contreaseña Incorrecta")
            return redirect('logear')

    return render(request,"App/login.html")

def salir(request):
    logout(request)
    return redirect('logear')