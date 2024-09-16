from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from .forms import RegistroForm, ObraForm
from .models import Obra, Artista, FavoritoObra, FavoritoArtista, Comprador, Usuario
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


def galeria(request):
    return render(request, 'galeria.html')


User = get_user_model()

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            if usuario is None:
                print("Usuario no creado correctamente")
                messages.error(request, f"Ha habido un problema con el registro")
                return redirect('registro')
            else:
                # Hashear la contraseña antes de guardar el usuario
                usuario.set_password(form.cleaned_data['password'])
                
                usuario.es_artista = form.cleaned_data.get('es_artista', False)
                usuario.es_comprador = form.cleaned_data.get('es_comprador', False)
                
                # validación: al menos uno debe estar marcado
                if not usuario.es_artista and not usuario.es_comprador:
                    messages.error(request, f"Al menos una casilla debe estar marcada: artista o comprador")
                    return redirect('registro')
                
                usuario.save()

                if usuario.es_artista:
                    Artista.objects.create(usuario=usuario)
                # Así son excluyentes
                elif usuario.es_comprador:
                    Comprador.objects.create(usuario=usuario)

                login(request, usuario)
                
                # Añadir mensaje de éxito
                messages.success(request, f"Registro exitoso. ¡Bienvenido {usuario.username}!")
                
                # Redirigir a la página de inicio
                return redirect('home')
        else:
            print("Errores de form:", form.errors)  # Depurar los errores del formulario
    else:
        form = RegistroForm()
    
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil(request):
    usuario = request.user
    # print(dir(usuario))
    es_usuario = User.objects.filter(username=usuario.username).exists()

    # DESCOMENTAR ESTAS DOS PROXIMAS LINEAAS
    es_artista = Artista.objects.filter(usuario=usuario).exists()

    es_comprador = Comprador.objects.filter(usuario=usuario).exists()

    # Aquí puedes obtener más datos relevantes, como las obras favoritas o los artistas favoritos
    # obras_favoritas = usuario.obras_favoritas.all()  # Si tienes un campo 'obras_favoritas' en el modelo Usuario
    # artistas_favoritos = usuario.artistas_favoritos.all()  # Si tienes un campo 'artistas_favoritos'

    context = {
        'usuario': usuario,
        'es_artista': es_artista,
        'es_comprador': es_comprador,
        # 'obras_favoritas': obras_favoritas,
        # 'artistas_favoritos': artistas_favoritos,
    }
    
    print(context)
    
    return render(request, 'perfil.html', context)

def detalle_obra(request, id):
    return render(request, 'detalle_obra.html', {'id':id})

@login_required
def subir_obra(request):
    if not Artista.objects.filter(usuario=request.user).exists():
        return redirect('perfil')  # Redirigir si no es un artista

    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.artista = Artista.objects.get(usuario=request.user)
            obra.save()
            return redirect('perfil')  # Redirigir al perfil después de subir
    else:
        form = ObraForm()

    return render(request, 'subir_obra.html', {'form': form})

def agregar_favorito_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    comprador = request.user.comprador
    FavoritoObra.objects.get_or_create(comprador=comprador, obra=obra)
    return redirect('detalle_obra', id=obra.id)

def eliminar_favorito_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    comprador = request.user.es_comprador
    favorito = get_object_or_404(FavoritoObra, comprador=comprador, obra=obra)
    favorito.delete()
    return redirect('detalle_obra', id=obra.id)

def agregar_favorito_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    comprador = request.user.es_comprador
    FavoritoArtista.objects.get_or_create(comprador=comprador, artista=artista)
    return redirect('perfil_artista', id=artista.id)

def eliminar_favorito_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    comprador = request.user.es_comprador
    favorito = get_object_or_404(FavoritoArtista, comprador=comprador, artista=artista)
    favorito.delete()
    return redirect('perfil_artista', id=artista.id)

@login_required
def obras_favoritas_view(request):
    obras_favoritas = request.user.obras_favoritas.all()
    return render(request, 'obras_favoritas.html', {'obras_favoritas': obras_favoritas})

@login_required
def artistas_favoritos_view(request):
    artistas_favoritos = request.user.artistas_favoritos.all()
    return render(request, 'artistas_favoritos.html', {'artistas_favoritos': artistas_favoritos})

