from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RecursoDigitalQuerySet(models.QuerySet):
    def visibles_para(self, usuario):
        """
        Regla 5: un usuario solo accede a recursos públicos (y publicados),
        a los suyos propios (en cualquier estado, para poder ver sus
        borradores) o a los que le compartieron y siguen con acceso activo.
        """
        publicos = models.Q(
            visibilidad=RecursoDigital.Visibilidad.PUBLICO,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
        if not usuario.is_authenticated:
            return self.filter(publicos).distinct()

        propios = models.Q(propietario=usuario)
        compartidos = models.Q(compartidos__usuario=usuario, compartidos__activo=True)
        return self.filter(publicos | propios | compartidos).distinct()

    def publicados(self):
        return self.filter(estado=RecursoDigital.Estado.PUBLICADO)


class RecursoDigital(models.Model):
    class Tipo(models.TextChoices):
        ORIGINAL = 'original', 'Original (creado en el Editor)'
        EXTERNO = 'externo', 'Externo (registrado)'

    class Visibilidad(models.TextChoices):
        PRIVADO = 'privado', 'Privado'
        PUBLICO = 'publico', 'Público'

    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        PUBLICADO = 'publicado', 'Publicado'

    # --- Datos obligatorios para publicar (Regla 1) ---
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='recursos',
        null=True,
        blank=True,
    )
    etiquetas = models.ManyToManyField(Etiqueta, related_name='recursos', blank=True)

    # --- Autoría (Regla 2): el autor puede no ser un usuario del sistema ---
    autor_texto = models.CharField(
        max_length=255,
        blank=True,
        help_text='Nombre del autor original, si no está registrado en el sistema.',
    )
    autor_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recursos_autoria',
    )

    # --- Responsable / propietario (Regla 3): siempre obligatorio ---
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recursos_propios',
    )

    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    contenido = models.TextField(
        blank=True,
        help_text='Contenido de recursos originales creados en el Editor.',
    )
    archivo = models.FileField(upload_to='recursos/', blank=True, null=True)

    visibilidad = models.CharField(
        max_length=20, choices=Visibilidad.choices, default=Visibilidad.PRIVADO
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.BORRADOR
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    objects = RecursoDigitalQuerySet.as_manager()

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    def clean(self):
        """
        Regla 1: no puede quedar publicado sin título, descripción,
        categoría y etiquetas.

        Nota: la validación de 'etiquetas' (M2M) no se puede hacer aquí
        de forma confiable si el objeto todavía no tiene pk (recurso
        nuevo sin guardar). Esa parte de la regla se valida en el
        ModelForm/vista del Editor, donde ya se cuenta con los datos
        del formulario antes de guardar la relación M2M.
        """
        if self.estado == self.Estado.PUBLICADO:
            faltantes = []
            if not self.titulo:
                faltantes.append('título')
            if not self.descripcion:
                faltantes.append('descripción')
            if not self.categoria_id:
                faltantes.append('categoría')
            if faltantes:
                raise ValidationError(
                    f"No se puede publicar: falta {', '.join(faltantes)}."
                )

    def tiene_autor_valido(self):
        """Regla 2: debe existir algún autor identificado (externo o de sistema)."""
        return bool(self.autor_texto or self.autor_usuario_id)