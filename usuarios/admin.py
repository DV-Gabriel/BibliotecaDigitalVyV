from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'rol', 'is_staff',
    )
    list_filter = UserAdmin.list_filter + ('rol',)

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'biografia')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol', 'biografia')}),
    )