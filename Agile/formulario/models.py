from django.db import models  

class Formulario(models.Model):  
    fdescripcion = models.CharField(max_length=100)  
    class Meta:  
        db_table = "formulario"  