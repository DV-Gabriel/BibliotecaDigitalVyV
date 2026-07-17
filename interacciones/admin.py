from django.contrib import admin

from .models import CompartidoCon


@admin.register(CompartidoCon)
class CompartidoConAdmin(admin.ModelAdmin):
    list_display = (
        'recurso', 'usuario', 'compartido_por', 'activo',
        'fecha_compartido', 'fecha_revocado',
    )
    list_filter = ('activo',)
    search_fields = (
        'recurso__titulo', 'usuario__username', 'compartido_por__username',
    )
    readonly_fields = ('fecha_compartido', 'fecha_revocado')
    autocomplete_fields = ('recurso', 'usuario', 'compartido_por')
    actions = ['revocar_acceso']

    @admin.action(description='Revocar acceso a los recursos seleccionados')
    def revocar_acceso(self, request, queryset):
        activos = queryset.filter(activo=True)
        for compartido in activos:
            compartido.revocar()
        self.message_user(request, f'{activos.count()} acceso(s) revocado(s).')