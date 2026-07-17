from django import forms
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class CompartirForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),
        label='Compartir con',
    )

    def __init__(self, *args, propietario=None, **kwargs):
        super().__init__(*args, **kwargs)
        if propietario is not None:
            # No tiene sentido compartir un recurso con uno mismo.
            self.fields['usuario'].queryset = Usuario.objects.exclude(pk=propietario.pk)
