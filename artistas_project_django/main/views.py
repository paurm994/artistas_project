from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import RegistroForm, ObraForm
from .models import Obra, Artista, FavoritoObra, FavoritoArtista

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
            login(request, usuario)
            return redirect('perfil')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form':form})

def perfil(request):
    return render(request, 'perfil.html')

def detalle_obra(request, id):
    return render(request, 'detalle_obra.html', {'id':id})

def subir_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.artista = request.user.artista
            obra.save()
            return redirect('perfil')
    else:
        form = ObraForm()
    return render(request, 'subir_obra.html', {'form':form})

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