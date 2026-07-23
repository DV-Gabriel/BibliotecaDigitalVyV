"""
Configuración de ambiente para los tests BDD con Behave y Django.

Este archivo se ejecuta antes de todos los tests y proporciona
hooks para setup/teardown de la base de datos y fixtures.
"""
import os
import django
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.test import Client
from django.test.utils import get_runner

# Evita doble inicialización de Django. Si el runner que lanza behave
# (p. ej. el plugin de Behave de PyCharm) ya llamó a django.setup(),
# no lo repetimos: hacerlo de nuevo puede re-ejecutar los módulos
# 'models.py' de cada app y duplicar el registro de modelos, lo que
# deja el ORM en un estado inconsistente (ej. FieldError raro en
# lookups como 'exact').
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BibliotecaDigital.settings')
if not apps.ready:
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
    # Behave no hereda el aislamiento transaccional de TestCase. Como la base
    # se crea una sola vez en before_all, hay que vaciarla explícitamente para
    # que los datos de un escenario no colisionen con los del siguiente.
    call_command('flush', verbosity=0, interactive=False)

    # Test client de Django: lo usan los steps de autenticación
    # (context.client.force_login(user)).
    context.client = Client()

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
