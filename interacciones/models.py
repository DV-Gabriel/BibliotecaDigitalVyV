from django.conf import settings
from django.db import models
from django.utils import timezone

from recursos_digitales.models import RecursoDigital


class CompartidoCon(models.Model):
    """
    Registra con quién se compartió un recurso (Regla 4).

    Se usa el campo 'activo' en vez de borrar el registro al revocar,
    para conservar el historial de a quién se le compartió y cuándo
    se le revocó el acceso.
    """

    recurso = models.ForeignKey(
        RecursoDigital, on_delete=models.CASCADE, related_name='compartidos'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recursos_compartidos_conmigo',
    )
    compartido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recursos_que_comparti',
    )
    fecha_compartido = models.DateTimeField(auto_now_add=True)
    fecha_revocado = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('recurso', 'usuario')
        verbose_name_plural = 'recursos compartidos'
        ordering = ['-fecha_compartido']

    def __str__(self):
        estado = 'activo' if self.activo else 'revocado'
        return f'{self.recurso} → {self.usuario} ({estado})'

    def revocar(self):
        """Regla 4: el propietario puede revocar el acceso en cualquier momento."""
        self.activo = False
        self.fecha_revocado = timezone.now()
        self.save(update_fields=['activo', 'fecha_revocado'])