import difflib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import RecursoExternoForm, RecursoOriginalForm
from .models import Categoria, Etiqueta, RecursoDigital

from espacio_personal.models import Coleccion, Favorito


def _buscar_similares(texto, queryset, umbral=0.6, limite=3):
    """
    Detección de similitud por contenido (característica 2).

    Comparación simple con difflib: suficiente para un catálogo de
    tamaño moderado. Si el volumen de recursos crece mucho, esto se
    reemplaza por TF-IDF/embeddings + una tarea async, sin tocar el
    resto de la vista.
    """
    candidatos = []
    for recurso in queryset.only('id', 'titulo', 'descripcion'):
        ratio = difflib.SequenceMatcher(
            None, texto.lower(), f'{recurso.titulo} {recurso.descripcion}'.lower()
        ).ratio()
        if ratio >= umbral:
            candidatos.append((ratio, recurso))
    candidatos.sort(key=lambda item: item[0], reverse=True)
    return [recurso for _, recurso in candidatos[:limite]]


class CatalogoListView(ListView):
    """
    Explorar y buscar recursos digitales en el catálogo (característica 1).

    Reusa RecursoDigital.objects.visibles_para(), que centraliza la
    Regla 5, y agrega sobre eso los filtros de búsqueda (texto,
    categoría, etiqueta).
    """

    model = RecursoDigital
    template_name = 'recursos_digitales/catalogo_list.html'
    context_object_name = 'recursos'
    paginate_by = 12

    def get_queryset(self):
        queryset = RecursoDigital.objects.visibles_para(self.request.user)

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q)
                | Q(descripcion__icontains=q)
                | Q(autor_texto__icontains=q)
            )

        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)

        etiqueta_id = self.request.GET.get('etiqueta')
        if etiqueta_id:
            queryset = queryset.filter(etiquetas__id=etiqueta_id)

        return queryset.select_related('categoria', 'propietario').prefetch_related(
            'etiquetas'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['etiquetas'] = Etiqueta.objects.all()
        # Se devuelven los filtros actuales para que el template pueda
        # mantenerlos seleccionados y armar los links de paginación.
        context['query'] = self.request.GET.get('q', '')
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        context['etiqueta_seleccionada'] = self.request.GET.get('etiqueta', '')
        return context


class RecursoDetailView(DetailView):
    """
    Detalle de un recurso. Usa el mismo filtro de visibilidad que el
    catálogo: si el recurso no es público/propio/compartido, Django
    devuelve 404 en lugar de un error de permisos, para no revelar
    que el recurso existe.
    """

    model = RecursoDigital
    template_name = 'recursos_digitales/recurso_detail.html'
    context_object_name = 'recurso'

    def get_queryset(self):
        return (
            RecursoDigital.objects.visibles_para(self.request.user)
            .select_related('categoria', 'propietario', 'autor_usuario')
            .prefetch_related('etiquetas')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['es_favorito'] = Favorito.objects.filter(
                usuario=user, recurso=self.object
            ).exists()
            context['colecciones_usuario'] = Coleccion.objects.filter(propietario=user)
            context['colecciones_con_recurso'] = set(
                self.object.colecciones.filter(propietario=user).values_list('id', flat=True)
            )
        return context


class RecursoOriginalCreateView(LoginRequiredMixin, CreateView):
    """El Editor (característica 2): crear un recurso original."""

    model = RecursoDigital
    form_class = RecursoOriginalForm
    template_name = 'recursos_digitales/recurso_original_form.html'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        form.instance.autor_usuario = self.request.user  # el creador es el autor
        response = super().form_valid(form)

        texto = f'{self.object.titulo} {self.object.descripcion} {self.object.contenido}'
        similares = _buscar_similares(
            texto,
            RecursoDigital.objects.filter(
                tipo=RecursoDigital.Tipo.ORIGINAL
            ).exclude(pk=self.object.pk),
        )
        if similares:
            nombres = ', '.join(r.titulo for r in similares)
            messages.warning(
                self.request,
                f'Se detectaron recursos similares ya existentes: {nombres}. '
                'Revisalos antes de publicar para evitar contenido duplicado.',
            )
        return response

    def get_success_url(self):
        return reverse_lazy('recursos_digitales:detalle', kwargs={'pk': self.object.pk})


class RecursoExternoCreateView(LoginRequiredMixin, CreateView):
    """Registrar un recurso de autor externo (característica 3)."""

    model = RecursoDigital
    form_class = RecursoExternoForm
    template_name = 'recursos_digitales/recurso_externo_form.html'

    def form_valid(self, form):
        form.instance.propietario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recursos_digitales:detalle', kwargs={'pk': self.object.pk})


class RecursoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Editar mis propios recursos (característica 4).

    Regla 6: el get_queryset restringido al propietario hace que
    cualquier intento de editar un recurso ajeno devuelva 404, sin
    necesidad de chequeos extra en el template ni en el POST.
    """

    model = RecursoDigital
    template_name = 'recursos_digitales/recurso_form.html'

    def get_queryset(self):
        return RecursoDigital.objects.filter(propietario=self.request.user)

    def get_form_class(self):
        if self.object.tipo == RecursoDigital.Tipo.ORIGINAL:
            return RecursoOriginalForm
        return RecursoExternoForm

    def get_success_url(self):
        return reverse_lazy('recursos_digitales:detalle', kwargs={'pk': self.object.pk})