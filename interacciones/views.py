from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from recursos_digitales.models import RecursoDigital

from .forms import CompartirForm
from .models import CompartidoCon


class CompartirRecursoView(LoginRequiredMixin, View):
    """
    Compartir un recurso con otro usuario (característica 8 / Regla 4).

    Solo el propietario puede compartir: se resuelve buscando el
    recurso restringido a propietario=request.user, igual que en
    RecursoUpdateView de recursos_digitales.
    """

    template_name = 'interacciones/compartir_form.html'

    def get_recurso(self, request, recurso_pk):
        return get_object_or_404(
            RecursoDigital, pk=recurso_pk, propietario=request.user
        )

    def get(self, request, recurso_pk):
        recurso = self.get_recurso(request, recurso_pk)
        form = CompartirForm(propietario=request.user)
        return render(request, self.template_name, {'recurso': recurso, 'form': form})

    def post(self, request, recurso_pk):
        recurso = self.get_recurso(request, recurso_pk)
        form = CompartirForm(request.POST, propietario=request.user)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            # update_or_create en vez de create: si antes se compartió
            # y después se revocó, este mismo registro se reactiva en
            # lugar de violar el unique_together (recurso, usuario).
            CompartidoCon.objects.update_or_create(
                recurso=recurso,
                usuario=usuario,
                defaults={
                    'compartido_por': request.user,
                    'activo': True,
                    'fecha_revocado': None,
                },
            )
            messages.success(request, f'Se compartió "{recurso.titulo}" con {usuario}.')
            return redirect('interacciones:compartidos_por_recurso', recurso_pk=recurso.pk)
        return render(request, self.template_name, {'recurso': recurso, 'form': form})


class CompartidosPorRecursoListView(LoginRequiredMixin, ListView):
    """
    Panel del propietario: a quién se compartió este recurso (activos
    e historial de revocados), con acceso directo a revocar cada uno.
    """

    model = CompartidoCon
    template_name = 'interacciones/compartidos_por_recurso.html'
    context_object_name = 'compartidos'

    def get_recurso(self):
        return get_object_or_404(
            RecursoDigital, pk=self.kwargs['recurso_pk'], propietario=self.request.user
        )

    def get_queryset(self):
        self.recurso = self.get_recurso()
        return CompartidoCon.objects.filter(recurso=self.recurso).select_related('usuario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recurso'] = self.recurso
        context['form'] = CompartirForm(propietario=self.request.user)
        return context


class RevocarAccesoView(LoginRequiredMixin, View):
    """
    Revocar acceso a un recurso propio (Regla 4).

    El filtro recurso__propietario=request.user impide que alguien
    revoque comparticiones de recursos ajenos adivinando el ID.
    """

    def post(self, request, pk):
        compartido = get_object_or_404(
            CompartidoCon, pk=pk, recurso__propietario=request.user, activo=True
        )
        compartido.revocar()
        messages.info(
            request,
            f'Se revocó el acceso de {compartido.usuario} a "{compartido.recurso.titulo}".',
        )
        return redirect('interacciones:compartidos_por_recurso', recurso_pk=compartido.recurso_id)


class RecursosCompartidosConmigoListView(LoginRequiredMixin, ListView):
    """Característica 9: recursos que otros usuarios compartieron conmigo."""

    template_name = 'interacciones/compartidos_conmigo.html'
    context_object_name = 'compartidos'

    def get_queryset(self):
        return (
            CompartidoCon.objects.filter(usuario=self.request.user, activo=True)
            .select_related('recurso', 'recurso__categoria', 'compartido_por')
        )