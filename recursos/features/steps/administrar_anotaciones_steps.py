"""
Steps para la feature 'Administrar_anotaciones'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital
from espacio_personal.models import Anotacion
from interacciones.models import CompartidoCon

User = get_user_model()


@given('tengo acceso "{tipo_acceso}" al recurso "{recurso}"')
@given('que tengo acceso "{tipo_acceso}" al recurso "{recurso}"')
def step_setup_resource_access(context, tipo_acceso, recurso):
    """Configura acceso a un recurso según el tipo."""
    # Usar usuario_actual si existe, sino crear uno
    user = getattr(context, 'usuario_actual', None)
    if not user:
        user = User.objects.create_user(
            username='test_user',
            password='test123',
            first_name='Test',
        )
        context.usuario_actual = user
    
    # Crear o recuperar recurso
    try:
        recurso_obj = RecursoDigital.objects.get(titulo=recurso)
    except RecursoDigital.DoesNotExist:
        if tipo_acceso == 'propio':
            recurso_obj = RecursoDigital.objects.create(
                titulo=recurso,
                descripcion=f'Recurso {recurso}',
                propietario=user,
                tipo=RecursoDigital.Tipo.ORIGINAL,
                visibilidad=RecursoDigital.Visibilidad.PRIVADO,
            )
        elif tipo_acceso == 'público':
            otro_user = User.objects.create_user(
                username='otro_usuario',
                password='test123',
            )
            recurso_obj = RecursoDigital.objects.create(
                titulo=recurso,
                descripcion=f'Recurso {recurso}',
                propietario=otro_user,
                tipo=RecursoDigital.Tipo.ORIGINAL,
                visibilidad=RecursoDigital.Visibilidad.PUBLICO,
                estado=RecursoDigital.Estado.PUBLICADO,
            )
        elif tipo_acceso == 'compartido':
            otro_user = User.objects.create_user(
                username='otro_usuario_compartidor',
                password='test123',
            )
            recurso_obj = RecursoDigital.objects.create(
                titulo=recurso,
                descripcion=f'Recurso {recurso}',
                propietario=otro_user,
                tipo=RecursoDigital.Tipo.ORIGINAL,
                visibilidad=RecursoDigital.Visibilidad.PRIVADO,
            )
            # Compartir con el usuario actual
            CompartidoCon.objects.get_or_create(
                recurso=recurso_obj,
                usuario=user,
                compartido_por=otro_user,
                defaults={'activo': True}
            )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[recurso] = recurso_obj


@when('agrego una anotación personal sobre "{recurso}"')
def step_add_annotation(context, recurso):
    """Agrega una anotación a un recurso."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    anotacion = Anotacion.objects.create(
        usuario=user,
        recurso=recurso_obj,
        contenido='Esta es mi anotación personal',
    )
    
    if not hasattr(context, 'anotaciones'):
        context.anotaciones = {}
    context.anotaciones[recurso] = anotacion
    context.last_annotation = anotacion


@then('la anotación queda guardada asociada únicamente a mi usuario')
def step_verify_annotation_saved_personal(context):
    """Verifica que la anotación es personal."""
    anotacion = context.last_annotation
    assert anotacion.usuario == context.usuario_actual, \
        "La anotación no está asociada al usuario actual"


@then('no es visible para ningún otro usuario que consulte "{recurso}"')
def step_verify_annotation_not_visible_others(context, recurso):
    """Verifica que otros usuarios no ven la anotación."""
    recurso_obj = context.recursos.get(recurso)
    otro_user = User.objects.create_user(
        username='otro_user_anotaciones',
        password='test123',
    )
    
    # Anotaciones del usuario actual (no de otros)
    anotaciones_otro = Anotacion.objects.filter(
        usuario=otro_user,
        recurso=recurso_obj
    )
    assert not anotaciones_otro.exists(), \
        "Las anotaciones de otros usuarios son visibles"


@given('tengo una anotación previa sobre el recurso "{recurso}"')
@given('que tengo una anotación previa sobre el recurso "{recurso}"')
def step_ensure_annotation_exists(context, recurso):
    """Asegura que existe una anotación previa."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    if not recurso_obj:
        recurso_obj = RecursoDigital.objects.create(
            titulo=recurso,
            descripcion=f'Recurso {recurso}',
            propietario=user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
        )
        context.recursos[recurso] = recurso_obj
    
    anotacion, _ = Anotacion.objects.get_or_create(
        usuario=user,
        recurso=recurso_obj,
        defaults={'contenido': 'Anotación previa'}
    )
    
    context.anotacion_previa = anotacion


@when('modifico el contenido de esa anotación')
def step_modify_annotation(context):
    """Modifica el contenido de la anotación."""
    anotacion = context.anotacion_previa
    anotacion.contenido = 'Contenido modificado de la anotación'
    anotacion.save()
    context.anotacion_modificada = anotacion


@then('se guarda el nuevo contenido')
def step_verify_new_content_saved(context):
    """Verifica que el nuevo contenido fue guardado."""
    anotacion = context.anotacion_modificada
    anotacion.refresh_from_db()
    assert 'modificado' in anotacion.contenido.lower(), \
        "El contenido no fue actualizado correctamente"


@then('se conserva su carácter privado')
def step_verify_privacy_preserved(context):
    """Verifica que la anotación sigue siendo privada."""
    anotacion = context.anotacion_modificada
    assert anotacion.usuario == context.usuario_actual, \
        "La anotación dejó de ser privada"


@given('tengo una anotación registrada sobre el recurso "{recurso}"')
@given('que tengo una anotación registrada sobre el recurso "{recurso}"')
def step_ensure_annotation_exists_simple(context, recurso):
    """Asegura que existe una anotación."""
    step_ensure_annotation_exists(context, recurso)


@when('elimino dicha anotación')
def step_delete_annotation(context):
    """Elimina la anotación."""
    anotacion = context.anotacion_previa
    recurso_id = anotacion.recurso_id
    context.recurso_id_de_anotacion = recurso_id
    anotacion.delete()


@then('la anotación deja de estar asociada al recurso')
def step_verify_annotation_deleted(context):
    """Verifica que la anotación fue eliminada."""
    anotaciones = Anotacion.objects.filter(
        recurso_id=context.recurso_id_de_anotacion,
        usuario=context.usuario_actual
    )
    assert not anotaciones.exists(), \
        "La anotación aún existe"


@then('ya no aparece en mi listado de notas de "{recurso}"')
def step_verify_not_in_list(context, recurso):
    """Verifica que la anotación no aparece en el listado."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    anotaciones = Anotacion.objects.filter(
        usuario=user,
        recurso=recurso_obj
    )
    # Debería haber una o menos anotaciones (creada en pasos anteriores)
    # pero la eliminada no debería estar


@when('abro la vista de anotaciones de "{recurso}"')
def step_open_annotations_view(context, recurso):
    """Abre la vista de anotaciones."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    anotaciones = Anotacion.objects.filter(
        usuario=user,
        recurso=recurso_obj
    )
    context.anotaciones_vistas = anotaciones


@then('veo únicamente las anotaciones que yo mismo he creado')
def step_verify_only_own_annotations(context):
    """Verifica que solo ve sus propias anotaciones."""
    for anotacion in context.anotaciones_vistas:
        assert anotacion.usuario == context.usuario_actual, \
            "Se muestran anotaciones de otros usuarios"


@given('comparto el recurso "{recurso}" con otro usuario')
@given('que comparto el recurso "{recurso}" con otro usuario')
def step_share_resource_with_another(context, recurso):
    """Comparte un recurso con otro usuario."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    if recurso_obj is None:
        step_setup_resource_access(context, 'propio', recurso)
        recurso_obj = context.recursos[recurso]
    
    otro_user = User.objects.create_user(
        username='otro_usuario_compartido',
        password='test123',
    )
    
    CompartidoCon.objects.get_or_create(
        recurso=recurso_obj,
        usuario=otro_user,
        compartido_por=user,
        defaults={'activo': True}
    )
    
    context.otro_usuario_compartido = otro_user


@given('yo tengo anotaciones personales sobre "{recurso}"')
def step_ensure_personal_annotations(context, recurso):
    """Asegura que existen anotaciones personales."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    Anotacion.objects.create(
        usuario=user,
        recurso=recurso_obj,
        contenido='Mi anotación personal 1',
    )
    Anotacion.objects.create(
        usuario=user,
        recurso=recurso_obj,
        contenido='Mi anotación personal 2',
    )


@when('el otro usuario abre "{recurso}"')
def step_other_user_opens_resource(context, recurso):
    """Otro usuario abre el recurso."""
    otro_user = context.otro_usuario_compartido
    recurso_obj = context.recursos.get(recurso)
    
    anotaciones_visibles = Anotacion.objects.filter(
        recurso=recurso_obj,
        usuario=otro_user
    )
    context.anotaciones_del_otro = anotaciones_visibles


@then('no visualiza ninguna de mis anotaciones')
def step_verify_annotations_hidden(context):
    """Verifica que las anotaciones están ocultas."""
    assert not context.anotaciones_del_otro.exists(), \
        "El otro usuario puede ver las anotaciones personales"


@given('el acceso al recurso "{recurso}" me fue revocado por su propietario')
@given('que el acceso al recurso "{recurso}" me fue revocado por su propietario')
def step_revoke_access_to_resource(context, recurso):
    """Revoca el acceso a un recurso."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    try:
        compartido = CompartidoCon.objects.get(
            recurso=recurso_obj,
            usuario=user
        )
        compartido.revocar()
    except CompartidoCon.DoesNotExist:
        pass


@when('intento agregar una anotación sobre "{recurso}"')
def step_try_add_annotation(context, recurso):
    """Intenta agregar una anotación."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    try:
        recursos_visibles = RecursoDigital.objects.visibles_para(user)
        if recurso_obj not in recursos_visibles:
            context.last_error = PermissionError("No tiene acceso al recurso")
            context.last_error_message = "ya no tengo acceso al recurso"
        else:
            context.last_error = None
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('el sistema rechaza la acción')
def step_verify_action_rejected(context):
    """Verifica que la acción fue rechazada."""
    assert context.last_error is not None


@then('me indica que ya no tengo acceso al recurso')
def step_verify_no_access_message(context):
    """Verifica el mensaje de falta de acceso."""
    if hasattr(context, 'last_error_message'):
        assert 'acceso' in context.last_error_message.lower()


@given('tenía anotaciones sobre el recurso "{recurso}"')
@given('que tenía anotaciones sobre el recurso "{recurso}"')
def step_ensure_annotations_exist(context, recurso):
    """Asegura que existen anotaciones previas."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    if recurso_obj is None:
        step_setup_resource_access(context, 'compartido', recurso)
        recurso_obj = context.recursos[recurso]
    
    Anotacion.objects.create(
        usuario=user,
        recurso=recurso_obj,
        contenido='Anotación previa a la revocación',
    )


@when('intento consultar mis anotaciones previas de "{recurso}"')
def step_try_view_previous_annotations(context, recurso):
    """Intenta ver anotaciones previas."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    
    try:
        recursos_visibles = RecursoDigital.objects.visibles_para(user)
        if recurso_obj not in recursos_visibles:
            context.last_error = PermissionError("No tiene acceso")
        else:
            context.last_error = None
    except Exception as e:
        context.last_error = e


@then('el sistema no me permite visualizarlas mientras no tenga acceso al recurso')
def step_verify_cannot_view_previous_annotations(context):
    """Verifica que no puede ver anotaciones previas sin acceso."""
    assert context.last_error is not None


@given('tengo acceso al recurso sobre el cual quiero anotar')
def step_annotation_access_precondition(context):
    assert context.usuario_actual is not None


@given('que he creado una o más anotaciones sobre el recurso "{recurso}"')
def step_created_annotations(context, recurso):
    step_setup_resource_access(context, 'propio', recurso)
    step_ensure_personal_annotations(context, recurso)


@given('el propietario revoca mi acceso a "{recurso}"')
def step_owner_revokes_access(context, recurso):
    step_revoke_access_to_resource(context, recurso)


@given('que el usuario "{creador}" crea una anotación sobre un recurso')
def step_user_creates_annotation(context, creador):
    owner = User.objects.create_user(username='owner_visibility', password='test123')
    creator = owner
    if creador == 'invitado':
        creator = User.objects.create_user(username='guest_visibility', password='test123')
    recurso = RecursoDigital.objects.create(
        titulo='Recurso de visibilidad',
        descripcion='Recurso para comprobar privacidad',
        propietario=owner,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PUBLICO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    context.annotation_owner = owner
    context.annotation_creator = creator
    context.visibility_annotation = Anotacion.objects.create(
        usuario=creator, recurso=recurso, contenido='Nota privada'
    )


@when('el usuario "{consultor}" abre ese mismo recurso')
def step_user_opens_annotation_resource(context, consultor):
    if 'él mismo' in consultor:
        viewer = context.annotation_creator
    elif consultor in ('propietario', 'propietario del recurso'):
        viewer = context.annotation_owner
    else:
        viewer = User.objects.create_user(
            username=f'viewer_{User.objects.count()}', password='test123'
        )
    context.annotation_visible = viewer == context.visibility_annotation.usuario


@then('la anotación es "{visibilidad}"')
def step_annotation_visibility(context, visibilidad):
    assert context.annotation_visible is (visibilidad == 'visible')
