from django import forms
from django.core.exceptions import ValidationError

from .models import RecursoDigital


class RecursoOriginalForm(forms.ModelForm):
    """
    El Editor: crear un recurso original (característica 2).

    El propietario y el autor_usuario se asignan en la vista
    (request.user) — el propio creador es el autor, así que no se
    piden acá.
    """

    class Meta:
        model = RecursoDigital
        fields = [
            'titulo', 'descripcion', 'categoria', 'etiquetas',
            'contenido', 'visibilidad', 'estado',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'contenido': forms.Textarea(attrs={'rows': 12}),
            'etiquetas': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super().clean()
        # Regla 1: acá sí podemos validar etiquetas, porque en un
        # ModelForm cleaned_data ya trae el queryset seleccionado
        # aunque el objeto todavía no exista en la base de datos.
        if (
            cleaned_data.get('estado') == RecursoDigital.Estado.PUBLICADO
            and not cleaned_data.get('etiquetas')
        ):
            raise ValidationError(
                'Debe asignar al menos una etiqueta para publicar el recurso.'
            )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo = RecursoDigital.Tipo.ORIGINAL
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class RecursoExternoForm(forms.ModelForm):
    """Registrar un recurso educativo de un autor externo (característica 3)."""

    class Meta:
        model = RecursoDigital
        fields = [
            'titulo', 'descripcion', 'categoria', 'etiquetas',
            'autor_texto', 'autor_usuario', 'archivo',
            'visibilidad', 'estado',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'etiquetas': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super().clean()

        # Regla 2: el autor puede ser externo (texto libre) o un
        # usuario del sistema, pero tiene que haber uno de los dos.
        if not cleaned_data.get('autor_texto') and not cleaned_data.get('autor_usuario'):
            raise ValidationError(
                'Debe indicar un autor: un nombre externo o un usuario registrado.'
            )

        # Regla 1, misma validación de etiquetas que en el Editor.
        if (
            cleaned_data.get('estado') == RecursoDigital.Estado.PUBLICADO
            and not cleaned_data.get('etiquetas')
        ):
            raise ValidationError(
                'Debe asignar al menos una etiqueta para publicar el recurso.'
            )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo = RecursoDigital.Tipo.EXTERNO
        if commit:
            instance.save()
            self.save_m2m()
        return instance