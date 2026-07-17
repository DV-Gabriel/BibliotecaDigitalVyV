from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Extiende el modelo de usuario de Django.

    El rol es solo metadato informativo: según la visión del sistema,
    no condiciona permisos ni comportamiento (docente y estudiante
    operan igual).
    """

    class Rol(models.TextChoices):
        ESTUDIANTE = 'estudiante', 'Estudiante'
        DOCENTE = 'docente', 'Docente'

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ESTUDIANTE,
    )
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.get_full_name() or self.username