"""
Steps comunes para todas las features (autenticación, creación de usuarios, etc.).
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital, Categoria, Etiqueta

User = get_user_model()


@given('que existen los usuarios "{nombres}"')
def step_create_multiple_users(context, nombres):
    """Crea múltiples usuarios separados por comas."""
    # El parámetro llega como: Ana", "Luis" y "Marta. Separar tanto comas
    # como la conjunción final; el split anterior registraba una sola clave
    # literal `Luis" y "Marta` y luego los demás steps recibían None.
    user_list = [
        n.strip()
        for n in nombres.replace('"', '').replace(' y ', ',').split(',')
    ]
    context.usuarios = {}
    for name in user_list:
        try:
            user = User.objects.get(username=name.lower())
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=name.lower(),
                password='test123',
                first_name=name,
            )
        context.usuarios[name] = user


@given('que soy un usuario autenticado en el sistema')
def step_authenticate_user(context):
    """Autentica al usuario actual."""
    if not getattr(context, 'usuario_actual', None):
        user = User.objects.create_user(
            username='usuario_test',
            password='test123',
            first_name='Usuario',
        )
        context.usuario_actual = user
    if not hasattr(context, 'usuarios'):
        context.usuarios = {}
    # El login se hace contra el test client de Django, no contra el
    # diccionario de usuarios.
    context.client.force_login(context.usuario_actual)


@given('el usuario "{nombre}" está autenticado en el sistema')
def step_authenticate_specific_user(context, nombre):
    """Autentica un usuario específico."""
    try:
        user = User.objects.get(username=nombre.lower())
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=nombre.lower(),
            password='test123',
            first_name=nombre,
        )
    if not hasattr(context, 'usuarios'):
        context.usuarios = {}
    context.usuarios[nombre] = user
    context.usuario_actual = user
    # Antes: context.usuarios.force_login(user) -> 'usuarios' es un dict,
    # no tiene force_login. El login va contra el test client.
    context.client.force_login(user)


@given('existe el usuario "{nombre}"')
@given('que existe el usuario "{nombre}"')
def step_ensure_user_exists(context, nombre):
    """Asegura que existe un usuario."""
    try:
        user = User.objects.get(username=nombre.lower())
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=nombre.lower(),
            password='test123',
            first_name=nombre,
        )
    if not hasattr(context, 'usuarios'):
        context.usuarios = {}
    context.usuarios[nombre] = user


@then('el usuario "{nombre}" debe tener acceso al recurso "{titulo}"')
def step_user_has_access(context, nombre, titulo):
    """Verifica que un usuario tiene acceso a un recurso."""
    usuario = context.usuarios.get(nombre)
    assert usuario is not None, f"Usuario {nombre} no existe"

    recurso = RecursoDigital.objects.get(titulo=titulo)
    # Verificar acceso mediante la queryset visibles_para
    recursos_visibles = RecursoDigital.objects.visibles_para(usuario)
    assert recurso in recursos_visibles, f"{nombre} no tiene acceso a {titulo}"


@then('el usuario "{nombre}" no debe tener acceso al recurso "{titulo}"')
def step_user_no_access(context, nombre, titulo):
    """Verifica que un usuario NO tiene acceso a un recurso."""
    usuario = context.usuarios.get(nombre)
    assert usuario is not None, f"Usuario {nombre} no existe"

    recurso = RecursoDigital.objects.get(titulo=titulo)
    recursos_visibles = RecursoDigital.objects.visibles_para(usuario)
    assert recurso not in recursos_visibles, f"{nombre} tiene acceso inesperado a {titulo}"


@then('el sistema debe rechazar la acción')
def step_action_rejected(context):
    """Verifica que la última acción fue rechazada."""
    if not hasattr(context, 'last_error'):
        raise AssertionError("Se esperaba un error pero la acción fue exitosa")
    assert context.last_error is not None


@then('debe mostrar un mensaje indicando que {mensaje}')
def step_check_error_message(context, mensaje):
    """Verifica el mensaje de error."""
    if hasattr(context, 'last_error_message'):
        assert mensaje.lower() in context.last_error_message.lower(), \
            f"Mensaje esperado: {mensaje}, obtenido: {context.last_error_message}"


@then('debe indicar que "{mensaje}"')
def step_verify_indicate_message_quoted(context, mensaje):
    """Step genérico para mensajes entre comillas."""
    if hasattr(context, 'last_error_message'):
        assert mensaje.lower() in context.last_error_message.lower(), \
            f"Mensaje esperado: {mensaje}, obtenido: {context.last_error_message}"


@then('debe indicar que {mensaje}')
def step_verify_indicate_message(context, mensaje):
    """Step genérico para mensajes sin comillas."""
    if hasattr(context, 'last_error_message'):
        assert mensaje.lower() in context.last_error_message.lower(), \
            f"Mensaje esperado: {mensaje}, obtenido: {context.last_error_message}"
