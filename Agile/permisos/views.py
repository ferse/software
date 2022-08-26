from django.shortcuts import render, redirect  
from permisos.forms import PermisoForm  
from permisos.models import Permiso

# Create your views here.  
def perm(request):  
    if request.method == "POST":  
        form = PermisoForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/permisos/show')  
            except:  
                pass  
    else:  
        form = PermisoForm()  
    return render(request,'permisos/index.html',{'form':form})  
def show(request):  
    permisos = Permiso.objects.all()  
    return render(request,"permisos/show.html",{'permisos':permisos})  
def edit(request, id):  
    permiso = Permiso.objects.get(id=id)  
    return render(request,'permisos/edit.html', {'permiso':permiso})  
def update(request, id):  
    permiso = Permiso.objects.get(id=id)  
    form = PermisoForm(request.POST, instance = permiso)  
    if form.is_valid():  
        form.save()  
        return redirect("/permisos/show")  
    return render(request, 'permisos/edit.html', {'permiso': permiso})  
def destroy(request, id):  
    permiso = Permiso.objects.get(id=id)  
    permiso.delete()  
    return redirect("/permisos/show")  