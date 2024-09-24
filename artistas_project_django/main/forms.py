from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Artista, Comprador, Obra

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'es_artista', 'es_comprador']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'descripcion', 'imagen', 'precio']