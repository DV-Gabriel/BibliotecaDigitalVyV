from django.conf import settings
from django.db import models

from recursos_digitales.models import RecursoDigital


class Coleccion(models.Model):
    """Colección/tablero personal de recursos (característica 5)."""

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='colecciones'
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    recursos = models.ManyToManyField(
        RecursoDigital, related_name='colecciones', blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('propietario', 'nombre')
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.propietario})'


class Favorito(models.Model):
    """Marcador de acceso rápido (característica 6)."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos'
    )
    recurso = models.ForeignKey(
        RecursoDigital,
        on_delete=models.CASCADE,
        related_name='marcado_como_favorito_por',
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'recurso')
        ordering = ['-fecha_agregado']

    def __str__(self):
        return f'{self.usuario} ♥ {self.recurso}'


class Anotacion(models.Model):
    """
    Notas personales sobre un recurso (característica 7).

    Regla 8: son de uso exclusivamente personal y nunca deben
    exponerse a otros usuarios, sin importar la visibilidad del
    recurso al que pertenecen. Esto se garantiza filtrando siempre
    por usuario=request.user en las vistas, no aquí en el modelo.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anotaciones'
    )
    recurso = models.ForeignKey(
        RecursoDigital, on_delete=models.CASCADE, related_name='anotaciones'
    )
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f'Nota de {self.usuario} sobre {self.recurso}'