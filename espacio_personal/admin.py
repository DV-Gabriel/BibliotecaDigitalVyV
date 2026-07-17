from django.contrib import admin

from .models import Anotacion, Coleccion, Favorito


@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'fecha_creacion')
    search_fields = ('nombre', 'propietario__username')
    filter_horizontal = ('recursos',)
    autocomplete_fields = ('propietario',)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'recurso', 'fecha_agregado')
    search_fields = ('usuario__username', 'recurso__titulo')
    autocomplete_fields = ('usuario', 'recurso')


@admin.register(Anotacion)
class AnotacionAdmin(admin.ModelAdmin):
    """
    Se registra solo para soporte/depuración de superusuarios.
    Regla 8: estas notas son personales y nunca deben exponerse en
    ninguna vista normal de la aplicación, solo aquí en el panel admin.
    """
    list_display = ('usuario', 'recurso', 'fecha_actualizacion')
    search_fields = ('usuario__username', 'recurso__titulo', 'contenido')
    autocomplete_fields = ('usuario', 'recurso')