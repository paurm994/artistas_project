from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('galeria/', views.galeria, name='galeria'),
    path('registro/', views.registro, name='registro'),
    path('perfil', views.perfil, name='perfil'),
    path('obra/<int:id>/', views.detalle_obra, name='detalle_obra'),
    # Añadir las rutas que hagan falta
]