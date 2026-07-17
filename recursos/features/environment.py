"""
Configuración de ambiente para los tests BDD con Behave y Django.

Este archivo se ejecuta antes de todos los tests y proporciona
hooks para setup/teardown de la base de datos y fixtures.
"""
import os
import django
from django.conf import settings
from django.test.utils import get_runner

# Asegurar que DJANGO_SETTINGS_MODULE esté definido antes de que se importen
# los módulos de steps que acceden a modelos. Esto se ejecuta al importar
# este archivo (antes de la carga de los step modules por behave).
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BibliotecaDigital.settings')
django.setup()


def before_all(context):
    """Se ejecuta una vez antes de todos los tests."""
    # Obtener el runner de tests de Django
    TestRunner = get_runner(settings)
    context.test_runner = TestRunner(verbosity=2, interactive=False, keepdb=True)
    
    # Crear la base de datos de tests
    context.old_config = context.test_runner.setup_test_environment()
    context.old_db = context.test_runner.setup_databases()


def after_all(context):
    """Se ejecuta una vez después de todos los tests."""
    context.test_runner.teardown_databases(context.old_db)
    context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    """Se ejecuta antes de cada escenario."""
    # Inicializar registries
    context.usuarios = {}
    context.recursos = {}
    context.colecciones = {}
    context.anotaciones = {}
    context.favoritos = {}
    
    # Inicializar estado
    context.last_error = None
    context.last_error_message = None
    context.usuario_actual = None


def after_scenario(context, scenario):
    """Se ejecuta después de cada escenario."""
    # Limpiar estado si es necesario
    pass


def before_step(context, step):
    """Se ejecuta antes de cada paso."""
    pass


def after_step(context, step):
    """Se ejecuta después de cada paso."""
    # Aquí se pueden manejar errores en pasos si es necesario
    pass
