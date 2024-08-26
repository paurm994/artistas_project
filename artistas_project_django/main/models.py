from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    es_artista = models.BooleanField(default=False)
    es_comprador = models.BooleanField(default=False)

class Artista(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True, null=True)
    # Más campos específicos del artista

class Comprador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    # Más campos específicos del comprador

class Obra(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='obras/')
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Más campos como tags, fecha creación... para la obra.