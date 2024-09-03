from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# Create your models here.

class Usuario(AbstractUser):
    es_artista = models.BooleanField(default=False)
    es_comprador = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios')

    groups = models.ManyToManyField(
        Group,
        related_name='usuarios', #Cambia related name para evitar conflictos

        blank=True,
        help_text=('Los grupos a los que pertenece este usuario. Un usuario obtendrá todos los permisos otorgados a cada uno de sus grupos.'),
        
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios',
        blank=True,
        help_text=('Permisos específicos para esta usuario.'),
        related_query_name='usuario',
    )

class Artista(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='artistas') 
    biografia = models.TextField(blank=True, null=True)
    # Más campos específicos del artista

class Comprador(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compradores')
    # Más campos específicos del comprador

class Obra(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='obras/')
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Más campos como tags, fecha creación... para la obra.

class FavoritoObra(models.Model):
    comprador = models.ForeignKey('Comprador', on_delete=models.CASCADE)
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE)
    fecha_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comprador', 'obra')

class FavoritoArtista(models.Model):
    comprador = models.ForeignKey('Comprador', on_delete=models.CASCADE)
    artista = models.ForeignKey('Artista', on_delete=models.CASCADE)
    fecha_favorito = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comprador', 'artista')