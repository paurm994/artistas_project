from django.contrib import admin
from .models import Usuario, Artista, Comprador, Obra

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Artista)
admin.site.register(Comprador)
admin.site.register(Obra)