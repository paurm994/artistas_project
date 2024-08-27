from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Artista, Comprador, Obra

class RegistroForm(UserCreationForm):
    es_artista = forms.BooleanField(required=False)
    es_comprador = forms.BooleanField(required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'es_artista', 'es_comprador', 'password1', 'password2']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if self.cleaned_data['es_artista']:
            usuario.es_artista = True
        elif self.cleaned_data['es_comprador']:
            usuario.es_comprador = True
        if commit:
            usuario.save()
            if usuario.es_artista:
                Artista.objects.create(usuario=usuario)
            if usuario.es_comprador:
                Comprador.objects.create(usuario=usuario)
            return usuario

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'descripcion', 'imagen', 'precio']