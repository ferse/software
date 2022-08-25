from django.shortcuts import render, redirect  
from formulario.forms import FormularioForm  
from formulario.models import Formulario  

# Create your views here.  
def emp(request):  
    if request.method == "POST":  
        form = FormularioForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except:  
                pass  
    else:  
        form = FormularioForm()  
    return render(request,'index.html',{'form':form})  
def show(request):  
    formularios = Formulario.objects.all()  
    return render(request,"formulario/show.html",{'formularios':formularios})  
def edit(request, id):  
    formulario = Formulario.objects.get(id=id)  
    return render(request,'edit.html', {'formulario':formulario})  
def update(request, id):  
    formulario = Formulario.objects.get(id=id)  
    form = FormularioForm(request.POST, instance = formulario)  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'formulario': formulario})  
def destroy(request, id):  
    formulario = Formulario.objects.get(id=id)  
    formulario.delete()  
    return redirect("/show")  