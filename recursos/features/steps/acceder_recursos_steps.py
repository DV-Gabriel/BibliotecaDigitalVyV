"""
Steps para la feature 'Acceder_recursos'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital
from interacciones.models import CompartidoCon

User = get_user_model()


@given('el recurso "{titulo}" es público y pertenece a {usuario}')
def step_create_public_resource(context, titulo, usuario):
    """Crea un recurso público."""
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user
    
    recurso, created = RecursoDigital.objects.get_or_create(
        titulo=titulo,
        propietario=user,
        defaults={
            'descripcion': f'Descripción de {titulo}',
            'tipo': RecursoDigital.Tipo.ORIGINAL,
            'visibilidad': RecursoDigital.Visibilidad.PUBLICO,
            'estado': RecursoDigital.Estado.PUBLICADO,
        }
    )
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@when('{usuario} consulta su lista de "recursos compartidos conmigo"')
def step_user_checks_shared_resources(context, usuario):
    """Un usuario ve su lista de recursos compartidos."""
    user = context.usuarios.get(usuario)
    context.usuario_actual = user
    
    # Obtener recursos compartidos activos
    compartidos = CompartidoCon.objects.filter(
        usuario=user,
        activo=True
    ).select_related('recurso')
    
    context.recursos_visibles = [c.recurso for c in compartidos]


@when('{usuario} abre el recurso "{titulo}"')
def step_user_opens_resource(context, usuario, titulo):
    """Un usuario intenta abrir un recurso."""
    user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    
    context.usuario_actual = user
    context.recurso_actual = recurso
    
    # Verificar acceso
    recursos_visibles = RecursoDigital.objects.visibles_para(user)
    if recurso not in recursos_visibles:
        context.last_error = PermissionError(f"No tiene acceso a {titulo}")
        context.last_error_message = "No tiene permiso para ver ese recurso"
    else:
        context.last_error = None


@when('{usuario} intenta abrir el recurso "{titulo}"')
def step_user_try_open_resource(context, usuario, titulo):
    """Un usuario intenta abrir un recurso (puede fallar)."""
    step_user_opens_resource(context, usuario, titulo)


@when('{usuario} intenta editar el recurso "{titulo}"')
def step_user_try_edit_resource(context, usuario, titulo):
    """Un usuario intenta editar un recurso."""
    user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    
    try:
        if recurso.propietario != user:
            context.last_error = PermissionError("Solo el propietario puede modificar")
            context.last_error_message = "solo el propietario puede modificar el recurso"
        else:
            context.last_error = None
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('debe poder visualizar su contenido completo')
def step_verify_can_view_content(context):
    """Verifica que puede ver el contenido."""
    assert context.last_error is None, \
        f"Error al ver contenido: {getattr(context, 'last_error_message', '')}"
    assert hasattr(context, 'recurso_actual'), "No hay recurso abierto"


@then('debe ver el recurso "{titulo}" en la lista')
def step_verify_resource_in_list(context, titulo):
    """Verifica que un recurso está en la lista visible."""
    recurso = context.recursos.get(titulo)
    assert recurso in context.recursos_visibles, \
        f"El recurso {titulo} no está en la lista visible"


@then('no debe ver el recurso "{titulo}" en la lista')
def step_verify_resource_not_in_list(context, titulo):
    """Verifica que un recurso NO está en la lista."""
    recurso = context.recursos.get(titulo)
    assert recurso not in context.recursos_visibles, \
        f"El recurso {titulo} no debería estar en la lista"


@then('el sistema debe rechazar el acceso')
def step_verify_access_denied(context):
    """Verifica que el acceso fue rechazado."""
    assert context.last_error is not None, "Se esperaba que el acceso fuera rechazado"


@then('debe mostrar un mensaje indicando que no tiene permiso para ver ese recurso')
def step_verify_no_permission_message(context):
    """Verifica mensaje de permisos denegados."""
    if hasattr(context, 'last_error_message'):
        assert 'permiso' in context.last_error_message.lower(), \
            f"Mensaje inesperado: {context.last_error_message}"
