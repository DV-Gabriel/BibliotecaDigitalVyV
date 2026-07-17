from django import forms

from .models import Anotacion, Coleccion


class ColeccionForm(forms.ModelForm):
    class Meta:
        model = Coleccion
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


class AnotacionForm(forms.ModelForm):
    class Meta:
        model = Anotacion
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }
