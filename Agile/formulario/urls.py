from django.contrib import admin  
from django.urls import path  
from formulario import views  
urlpatterns = [    
    path('formulario/form', views.new),  
    path('formulario/show',views.show),  
    path('formulario/edit/<int:id>', views.edit),  
    path('formulario/update/<int:id>', views.update),  
    path('formulario/delete/<int:id>', views.destroy),  
]  