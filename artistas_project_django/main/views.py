from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegistroForm, ObraForm
from .models import Obra, Artista, FavoritoObra, FavoritoArtista, Comprador, Usuario
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'home.html')

def galeria(request):
    return render(request, 'galeria.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            print(usuario)
            # Usuario.objects.create(user=usuario) # Verificar si el usuario es un Artista o Comprador
            # es_artista = form.cleaned_data.get('es_artista', False) 
            # es_comprador = form.cleaned_data.get('es_comprador', False) 
            # if es_artista: 
            #     Artista.objects.create(usuario=usuario, nombre_artistico=form.cleaned_data.get('nombre_artistico')) 
            # elif es_comprador: 
            #     Comprador.objects.create(usuario=usuario, nombre_completo=form.cleaned_data.get('nombre_completo')) # Autenticar y redirigir al usuario a la página de inicio
            login(request, usuario)
            print(f"Te has autenticado: {request.user.is_authenticated}")  # Depuración
            return redirect('perfil')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form':form})

@login_required
def perfil(request):
    usuario = request.user
    print(dir(usuario))
    # es_artista = Artista.objects.filter(usuario=usuario).exists()
    es_usuario = User.objects.filter(username=usuario.username).exists()

    # es_comprador = Comprador.objects.filter(usuario=usuario).exists()

    # Aquí puedes obtener más datos relevantes, como las obras favoritas o los artistas favoritos
    # obras_favoritas = usuario.obras_favoritas.all()  # Si tienes un campo 'obras_favoritas' en el modelo Usuario
    # artistas_favoritos = usuario.artistas_favoritos.all()  # Si tienes un campo 'artistas_favoritos'

    return render(request, 'perfil.html', {
        'usuario': usuario,
        # 'es_artista': es_artista,
        # 'es_comprador': es_comprador,
        # 'obras_favoritas': obras_favoritas,
        # 'artistas_favoritos': artistas_favoritos,
    })

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
    comprador = request.user.comprador
    favorito = get_object_or_404(FavoritoObra, comprador=comprador, obra=obra)
    favorito.delete()
    return redirect('detalle_obra', id=obra.id)

def agregar_favorito_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    comprador = request.user.comprador
    FavoritoArtista.objects.get_or_create(comprador=comprador, artista=artista)
    return redirect('perfil_artista', id=artista.id)

def eliminar_favorito_artista(request, artista_id):
    artista = get_object_or_404(Artista, id=artista_id)
    comprador = request.user.comprador
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

