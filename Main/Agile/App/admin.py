from django.contrib import admin
from App.models import Usuario, Estado_Us, Estado_Proyecto, Estado_Sprint

admin.site.register(Usuario)
admin.site.register(Estado_Us)
admin.site.register(Estado_Proyecto)
admin.site.register(Estado_Sprint)