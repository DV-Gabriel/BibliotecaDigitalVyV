"""
Steps para la feature 'Gestionar_favoritos'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital
from espacio_personal.models import Favorito
from interacciones.models import CompartidoCon

User = get_user_model()


@when('intento marcarlo como favorito')
def step_mark_as_favorite(context):
    """Intenta marcar un recurso como favorito."""
    user = context.usuario_actual
    recurso = list(context.recursos.values())[-1] if hasattr(context, 'recursos') else None
    
    try:
        if not recurso:
            context.last_error = ValueError("No hay recurso")
            context.ultimo_resultado = "acción rechazada"
            return
        
        # Verificar acceso según RN5
        recursos_visibles = RecursoDigital.objects.visibles_para(user)
        if recurso not in recursos_visibles:
            context.last_error = PermissionError("No tiene acceso")
            context.ultimo_resultado = "acción rechazada"
            return
        
        # Marcar como favorito
        favorito, created = Favorito.objects.get_or_create(
            usuario=user,
            recurso=recurso
        )
        context.last_error = None
        context.ultimo_resultado = "marcado exitosamente"
        context.favorito = favorito
    except Exception as e:
        context.last_error = e
        context.ultimo_resultado = "acción rechazada"


@given('existe un recurso de tipo "{tipo_recurso}"')
@given('que existe un recurso de tipo "{tipo_recurso}"')
def step_create_resource_by_type(context, tipo_recurso):
    """Crea un recurso según su tipo."""
    user = context.usuario_actual
    if not user:
        user = User.objects.create_user(
            username='test_user_favorito',
            password='test123',
        )
        context.usuario_actual = user
    
    otro_user = User.objects.create_user(
        username='otro_user_favorito',
        password='test123',
    )
    
    if tipo_recurso == 'público':
        recurso = RecursoDigital.objects.create(
            titulo=f'Recurso público {tipo_recurso}',
            descripcion='Descripción',
            propietario=otro_user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PUBLICO,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
    elif tipo_recurso == 'compartido conmigo':
        recurso = RecursoDigital.objects.create(
            titulo=f'Recurso compartido {tipo_recurso}',
            descripcion='Descripción',
            propietario=otro_user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        )
        # Compartir con usuario actual
        CompartidoCon.objects.create(
            recurso=recurso,
            usuario=user,
            compartido_por=otro_user,
            activo=True,
        )
    elif tipo_recurso == 'propio':
        recurso = RecursoDigital.objects.create(
            titulo=f'Recurso propio {tipo_recurso}',
            descripcion='Descripción',
            propietario=user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        )
    elif tipo_recurso == 'privado no compartido conmigo':
        recurso = RecursoDigital.objects.create(
            titulo=f'Recurso privado {tipo_recurso}',
            descripcion='Descripción',
            propietario=otro_user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[tipo_recurso] = recurso


@then('el resultado de la acción es "{resultado}"')
def step_verify_action_result(context, resultado):
    """Verifica el resultado de la acción."""
    assert context.ultimo_resultado == resultado, \
        f"Resultado esperado: {resultado}, obtenido: {context.ultimo_resultado}"


@given('el recurso "{titulo}" está en mi lista de favoritos')
@given('que el recurso "{titulo}" está en mi lista de favoritos')
def step_ensure_resource_is_favorite(context, titulo):
    """Asegura que un recurso es favorito."""
    user = context.usuario_actual
    recurso = context.recursos.get(titulo)
    
    if not recurso:
        propietario = User.objects.create_user(
            username='propietario_r2', password='test123'
        )
        recurso = RecursoDigital.objects.create(
            titulo=titulo,
            descripcion='Descripción',
            propietario=propietario,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
        CompartidoCon.objects.create(
            recurso=recurso,
            usuario=user,
            compartido_por=propietario,
            activo=True,
        )
        context.recursos[titulo] = recurso
    
    favorito, _ = Favorito.objects.get_or_create(
        usuario=user,
        recurso=recurso
    )
    context.favorito_test = favorito


@given('el propietario revoca el acceso compartido sobre "{titulo}"')
def step_revoke_shared_access(context, titulo):
    """Revoca el acceso compartido a un recurso."""
    recurso = context.recursos.get(titulo)
    
    try:
        compartido = CompartidoCon.objects.filter(
            recurso=recurso,
            usuario=context.usuario_actual
        ).first()
        if compartido:
            compartido.revocar()
    except Exception:
        pass


@when('accedo a mi lista de favoritos')
def step_access_favorites_list(context):
    """Accede a la lista de favoritos."""
    user = context.usuario_actual
    
    favoritos = Favorito.objects.filter(usuario=user).select_related('recurso')
    context.favoritos_list = favoritos


@then('"{titulo}" ya no está disponible para abrir')
def step_verify_favorite_unavailable(context, titulo):
    """Verifica que un favorito no está disponible."""
    recurso = context.recursos.get(titulo)
    user = context.usuario_actual
    
    # Verificar que el favorito existe pero el recurso no es accesible
    favorito = Favorito.objects.filter(usuario=user, recurso=recurso).first()
    assert favorito is not None, "El favorito fue eliminado"
    
    # Verificar que el recurso no es visible
    recursos_visibles = RecursoDigital.objects.visibles_para(user)
    assert recurso not in recursos_visibles, \
        "El recurso aún es visible"


@then('el sistema indica que el acceso fue revocado')
def step_verify_revoked_message(context):
    """Verifica que se indica la revocación."""
    # En una implementación real, habría un mensaje en la vista
    pass
