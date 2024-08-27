from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import agregar_favorito_obra, eliminar_favorito_obra, agregar_favorito_artista, eliminar_favorito_artista

urlpatterns = [
    path('', views.home, name='home'),
    path('galeria/', views.galeria, name='galeria'),
    path('registro/', views.registro, name='registro'),
    path('perfil', views.perfil, name='perfil'),
    path('obra/<int:id>/', views.detalle_obra, name='detalle_obra'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('favorito/obra/agregar/<int:obra_id>/', agregar_favorito_obra, name='agregar_favorito_obra'),
    path('favorito/obra/eliminar/<int:obra_id>/', eliminar_favorito_obra, name='eliminar_favorito_obra'),
    path('favorito/artista/agregar/<int:artista_id>/', agregar_favorito_artista, name='agregar_favorito_artista'),
    path('favorito/artista/eliminar/<int:artista_id>/', eliminar_favorito_artista, name='eliminar_favorito_artista'),
    # Añadir las rutas que hagan falta
]