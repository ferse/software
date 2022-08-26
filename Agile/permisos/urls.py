from django.contrib import admin  
from django.urls import path  
from permisos import views 

urlpatterns = [   
    path('permisos/perm', views.perm),  
    path('permisos/show',views.show),  
    path('permisos/edit/<int:id>', views.edit),  
    path('permisos/update/<int:id>', views.update),  
    path('permisos/delete/<int:id>', views.destroy),  
]  