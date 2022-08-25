from django import forms  

from formulario.models import Formulario  
class FormularioForm(forms.ModelForm):  
    class Meta:  
        model = Formulario  
        fields = "__all__"  