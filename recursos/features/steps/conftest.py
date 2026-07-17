"""
Configuración y fixtures comunes para los steps de BDD.
"""
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_registry():
    """Registry para almacenar usuarios creados durante los tests."""
    return {}


@pytest.fixture
def resource_registry():
    """Registry para almacenar recursos creados durante los tests."""
    return {}


@pytest.fixture
def error_registry():
    """Registry para almacenar errores/excepciones durante los tests."""
    return {}


def crear_usuario(username, full_name=""):
    """Utilidad para crear un usuario."""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            password='test123',
            first_name=full_name.split()[0] if full_name else username,
            last_name=' '.join(full_name.split()[1:]) if full_name and ' ' in full_name else '',
        )
    return user
