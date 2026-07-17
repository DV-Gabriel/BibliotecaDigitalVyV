from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from recursos_digitales.models import RecursoDigital

from .forms import AnotacionForm, ColeccionForm
from .models import Anotacion, Coleccion, Favorito


# ---------- Colecciones (característica 5) ----------

class ColeccionListView(LoginRequiredMixin, ListView):
    """Las colecciones son personales: cada usuario ve solo las suyas."""

    model = Coleccion
    template_name = 'espacio_personal/coleccion_list.html'
    context_object_name = 'colecciones'

    def get_queryset(self):
        return Coleccion.objects.filter(propietario=self.request.user)


class ColeccionDetailView(LoginRequiredMixin, DetailView):
    model = Coleccion
    template_name = 'espacio_personal/coleccion_detail.html'
    context_object_name = 'coleccion'

    def get_queryset(self):
        # Ni siquiera si algún recurso adentro es público se expone la
        # colección en sí: es un agrupamiento personal.
        return Coleccion.objects.filter(propietario=self.request.user)


class ColeccionCreateView(LoginRequiredMixin, CreateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'espacio_personal/coleccion_form.html'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('espacio_personal:coleccion_detalle', kwargs={'pk': self.object.pk})


class ColeccionUpdateView(LoginRequiredMixin, UpdateView):
    model = Coleccion
    form_class = ColeccionForm
    template_name = 'espacio_personal/coleccion_form.html'

    def get_queryset(self):
        return Coleccion.objects.filter(propietario=self.request.user)

    def get_success_url(self):
        return reverse('espacio_personal:coleccion_detalle', kwargs={'pk': self.object.pk})


class ColeccionDeleteView(LoginRequiredMixin, DeleteView):
    model = Coleccion
    template_name = 'espacio_personal/coleccion_confirm_delete.html'
    success_url = reverse_lazy('espacio_personal:coleccion_lista')

    def get_queryset(self):
        return Coleccion.objects.filter(propietario=self.request.user)


class ColeccionRecursoToggleView(LoginRequiredMixin, View):
    """
    Agrega o quita un recurso de una colección propia (POST, botón
    "guardar en colección" desde el detalle de un recurso).

    Solo se puede coleccionar lo que ya se puede ver (Regla 5): el
    get_object_or_404 sobre visibles_para() bloquea intentos de
    agregar recursos privados ajenos por ID adivinado.
    """

    def post(self, request, coleccion_pk, recurso_pk):
        coleccion = get_object_or_404(
            Coleccion, pk=coleccion_pk, propietario=request.user
        )
        recurso = get_object_or_404(
            RecursoDigital.objects.visibles_para(request.user), pk=recurso_pk
        )

        if coleccion.recursos.filter(pk=recurso.pk).exists():
            coleccion.recursos.remove(recurso)
            messages.info(request, f'Se quitó "{recurso.titulo}" de "{coleccion.nombre}".')
        else:
            coleccion.recursos.add(recurso)
            messages.success(request, f'Se agregó "{recurso.titulo}" a "{coleccion.nombre}".')

        return redirect('espacio_personal:coleccion_detalle', pk=coleccion.pk)


# ---------- Favoritos (característica 6) ----------

class FavoritoListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = 'espacio_personal/favorito_list.html'
    context_object_name = 'favoritos'

    def get_queryset(self):
        return (
            Favorito.objects.filter(usuario=self.request.user)
            .select_related('recurso', 'recurso__categoria')
        )


class FavoritoToggleView(LoginRequiredMixin, View):
    """Marca/desmarca un recurso como favorito. Botón único (POST), idempotente."""

    def post(self, request, recurso_pk):
        recurso = get_object_or_404(
            RecursoDigital.objects.visibles_para(request.user), pk=recurso_pk
        )
        favorito, creado = Favorito.objects.get_or_create(
            usuario=request.user, recurso=recurso
        )
        if not creado:
            favorito.delete()
            messages.info(request, f'"{recurso.titulo}" se quitó de favoritos.')
        else:
            messages.success(request, f'"{recurso.titulo}" se agregó a favoritos.')

        siguiente = request.POST.get('next') or reverse(
            'recursos_digitales:detalle', kwargs={'pk': recurso.pk}
        )
        return redirect(siguiente)


# ---------- Anotaciones (característica 7 / Regla 8) ----------

class AnotacionListView(LoginRequiredMixin, ListView):
    """
    Notas personales sobre un recurso puntual.

    Regla 8: SIEMPRE filtradas por usuario=request.user, sin excepción,
    sin importar si el recurso es público, privado o de otro dueño.
    Nunca se debe quitar ese filtro para "mostrar todas las notas".
    """

    model = Anotacion
    template_name = 'espacio_personal/anotacion_list.html'
    context_object_name = 'anotaciones'

    def get_recurso(self):
        return get_object_or_404(
            RecursoDigital.objects.visibles_para(self.request.user),
            pk=self.kwargs['recurso_pk'],
        )

    def get_queryset(self):
        self.recurso = self.get_recurso()
        return Anotacion.objects.filter(usuario=self.request.user, recurso=self.recurso)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recurso'] = self.recurso
        context['form'] = AnotacionForm()
        return context


class AnotacionCreateView(LoginRequiredMixin, CreateView):
    model = Anotacion
    form_class = AnotacionForm
    template_name = 'espacio_personal/anotacion_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.recurso = get_object_or_404(
            RecursoDigital.objects.visibles_para(request.user),
            pk=kwargs['recurso_pk'],
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.recurso = self.recurso
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('espacio_personal:anotaciones', kwargs={'recurso_pk': self.recurso.pk})


class AnotacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Anotacion
    form_class = AnotacionForm
    template_name = 'espacio_personal/anotacion_form.html'

    def get_queryset(self):
        # Regla 8 aplicada también a la edición: nadie edita notas ajenas.
        return Anotacion.objects.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse('espacio_personal:anotaciones', kwargs={'recurso_pk': self.object.recurso_id})


class AnotacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Anotacion
    template_name = 'espacio_personal/anotacion_confirm_delete.html'

    def get_queryset(self):
        return Anotacion.objects.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse('espacio_personal:anotaciones', kwargs={'recurso_pk': self.object.recurso_id})