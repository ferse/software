from django import forms  
from permisos.models import Permiso
  
class PermisoForm(forms.ModelForm):  
    class Meta:  
        model = Permiso  
        fields = "__all__"  