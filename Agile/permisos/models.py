from django.db import models
from formulario.models import Formulario 


class Permiso(models.Model):  
    pname = models.CharField(max_length=100)  
    pdescripcion = models.CharField(max_length=100)
    fid = models.ForeignKey(Formulario,related_name="related_form",on_delete=models.CASCADE)
    class Meta:  
        db_table = "permiso" 