from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistroForm
from .models import Usuario


class RegistroCreateView(CreateView):
    """
    Alta de un nuevo usuario. Cualquier visitante sin sesión puede
    acceder (no lleva LoginRequiredMixin, a diferencia de casi todas
    las otras vistas del sistema).
    """

    model = Usuario
    form_class = RegistroForm
    template_name = 'usuarios/registro_form.html'
    success_url = reverse_lazy('recursos_digitales:catalogo')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Autologuea al usuario recién creado: evita el paso extra de
        # pedirle que inicie sesión manualmente justo después de
        # registrarse.
        login(self.request, self.object)
        return response