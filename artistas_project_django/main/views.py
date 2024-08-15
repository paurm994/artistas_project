from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def galeria(request):
    return render(request, 'galeria.html')

def registro(request):
    return render(request, 'registro.html')

def perfil(request):
    return render(request, 'perfil.html')

def detalle_obra(request, id):
    return render(request, 'detalle_obra.html', {'id':id})