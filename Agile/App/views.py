from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,"App/index.html")

def logear(request):
    if request.method == 'POST':
        alias = request.POST['usuario']
        contra = request.POST['password']

        user = authenticate(username=alias, password=contra)

        if user is not None:
            login(request, user)
            return redirect('dashboard/')
        else:
            messages.error(request, "Usuario o contreaseña Incorrecta")
            return redirect('logear')

    return render(request,"App/login.html")