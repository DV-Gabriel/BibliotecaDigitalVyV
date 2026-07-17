from django.contrib import admin

from .models import Categoria, Etiqueta, RecursoDigital


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(RecursoDigital)
class RecursoDigitalAdmin(admin.ModelAdmin):
    list_display = (
        'titulo', 'propietario', 'categoria', 'tipo',
        'visibilidad', 'estado', 'fecha_creacion',
    )
    list_filter = ('tipo', 'visibilidad', 'estado', 'categoria')
    search_fields = ('titulo', 'descripcion', 'autor_texto', 'propietario__username')
    filter_horizontal = ('etiquetas',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    # Requiere que Usuario, Categoria tengan search_fields definidos (ya lo tienen).
    autocomplete_fields = ('propietario', 'autor_usuario', 'categoria')



