from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        # UserCreationForm ya agrega password1/password2 automáticamente,
        # acá solo extendemos los campos "de datos" del modelo.
        fields = ('username', 'email', 'rol', 'first_name', 'last_name')
