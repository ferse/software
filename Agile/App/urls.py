from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'App'

urlpatterns = [
    path('', views.home, name='index'),
    path('logout', views.home, name='logout'),
    path('dashboard', views.home, name='dashboard'),
    path('logear', views.logear, name='logear'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)