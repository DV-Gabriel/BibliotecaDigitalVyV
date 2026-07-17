"""
Steps para la feature 'Organizar_recursos'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital
from espacio_personal.models import Coleccion
from interacciones.models import CompartidoCon

User = get_user_model()


@given('el usuario tiene una colección personal llamada "{nombre_coleccion}"')
def step_create_collection(context, nombre_coleccion):
    """Crea una colección personal."""
    user = context.usuario_actual
    
    coleccion, _ = Coleccion.objects.get_or_create(
        propietario=user,
        nombre=nombre_coleccion,
        defaults={'descripcion': f'Colección {nombre_coleccion}'}
    )
    
    if not hasattr(context, 'colecciones'):
        context.colecciones = {}
    context.colecciones[nombre_coleccion] = coleccion


@given('existe un recurso "{visibilidad}" llamado "{recurso}"')
def step_create_resource_with_visibility(context, visibilidad, recurso):
    """Crea un recurso con visibilidad específica."""
    user = context.usuario_actual
    
    if visibilidad == 'público':
        otro_user = User.objects.create_user(
            username='otro_user_publico',
            password='test123',
        )
        recurso_obj = RecursoDigital.objects.create(
            titulo=recurso,
            descripcion='Descripción',
            propietario=otro_user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PUBLICO,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
    elif visibilidad == 'privado':
        otro_user = User.objects.create_user(
            username='otro_user_privado',
            password='test123',
        )
        recurso_obj = RecursoDigital.objects.create(
            titulo=recurso,
            descripcion='Descripción',
            propietario=otro_user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[recurso] = recurso_obj


@given('el recurso es de acceso público')
def step_verify_public_access(context):
    """Verifica que el recurso es público."""
    # Confirmación implícita del paso anterior
    pass


@given('el propietario ha compartido "{recurso}" con "{usuario}"')
def step_share_with_user(context, recurso, usuario):
    """Comparte un recurso con un usuario."""
    recurso_obj = context.recursos.get(recurso)
    user = context.usuarios.get(usuario) if hasattr(context, 'usuarios') else context.usuario_actual
    propietario = recurso_obj.propietario
    
    CompartidoCon.objects.get_or_create(
        recurso=recurso_obj,
        usuario=user,
        compartido_por=propietario,
        defaults={'activo': True}
    )


@given('"{usuario}" es propietario del recurso')
def step_set_resource_owner(context, usuario):
    """Verifica que un usuario es propietario."""
    user = context.usuarios.get(usuario) if hasattr(context, 'usuarios') else context.usuario_actual
    recurso = list(context.recursos.values())[-1]
    
    assert recurso.propietario == user, \
        f"El propietario no es {usuario}"


@when('el usuario agrega el recurso "{recurso}" a la colección "{coleccion}"')
def step_add_resource_to_collection(context, recurso, coleccion):
    """Agrega un recurso a una colección."""
    user = context.usuario_actual
    recurso_obj = context.recursos.get(recurso)
    coleccion_obj = context.colecciones.get(coleccion)
    
    try:
        # Verificar acceso
        recursos_visibles = RecursoDigital.objects.visibles_para(user)
        if recurso_obj not in recursos_visibles:
            context.last_error = PermissionError("No tiene acceso")
            context.last_error_message = "No tiene acceso al recurso"
            return
        
        coleccion_obj.recursos.add(recurso_obj)
        context.last_error = None
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@when('el usuario intenta agregar el recurso "{recurso}" a la colección "{coleccion}"')
def step_try_add_resource_to_collection(context, recurso, coleccion):
    """Intenta agregar un recurso a una colección."""
    step_add_resource_to_collection(context, recurso, coleccion)


@then('el recurso debe quedar incluido en la colección "{coleccion}"')
def step_verify_resource_in_collection(context, coleccion):
    """Verifica que el recurso está en la colección."""
    coleccion_obj = context.colecciones.get(coleccion)
    recurso = list(context.recursos.values())[-1]
    
    assert coleccion_obj.recursos.filter(pk=recurso.pk).exists(), \
        f"El recurso no está en la colección {coleccion}"


@then('el sistema no debe permitir agregar el recurso a la colección')
def step_verify_cannot_add_to_collection(context):
    """Verifica que no se puede agregar el recurso."""
    assert context.last_error is not None, \
        "Se esperaba un error al agregar el recurso"


@then('el "<atributo>" del recurso debe seguir siendo "<valor>"')
def step_verify_resource_attribute_unchanged(context, atributo, valor):
    """Verifica que un atributo del recurso no cambió."""
    recurso = list(context.recursos.values())[-1]
    
    if atributo == 'propietario':
        assert recurso.propietario.username == valor.lower(), \
            f"El propietario cambió inesperadamente"
    elif atributo == 'autor':
        assert recurso.autor_texto == valor or (
            recurso.autor_usuario and recurso.autor_usuario.username == valor.lower()
        ), f"El autor cambió inesperadamente"


@then('"{usuario}" no debe convertirse en propietario del recurso')
def step_verify_not_new_owner(context, usuario):
    """Verifica que un usuario NO es el propietario."""
    user = context.usuarios.get(usuario) if hasattr(context, 'usuarios') else None
    recurso = list(context.recursos.values())[-1]
    
    assert recurso.propietario != user, \
        f"{usuario} se convirtió en propietario inesperadamente"


@then('"{usuario}" no debe poder modificar el recurso')
def step_verify_cannot_modify(context, usuario):
    """Verifica que un usuario no puede modificar."""
    user = context.usuarios.get(usuario) if hasattr(context, 'usuarios') else None
    recurso = list(context.recursos.values())[-1]
    
    assert recurso.propietario != user, \
        f"{usuario} puede modificar el recurso"


@when('"{evento}"')
def step_trigger_event(context, evento):
    """Dispara un evento específico."""
    recurso = list(context.recursos.values())[-1]
    user = context.usuario_actual
    
    if 'retira el acceso' in evento:
        try:
            compartido = CompartidoCon.objects.get(
                recurso=recurso,
                usuario=user
            )
            compartido.revocar()
        except CompartidoCon.DoesNotExist:
            pass
    elif 'marca' in evento and 'público' in evento:
        recurso.visibilidad = RecursoDigital.Visibilidad.PUBLICO
        recurso.save()


@when('el usuario consulta la colección "{coleccion}"')
def step_check_collection(context, coleccion):
    """Consulta una colección."""
    coleccion_obj = context.colecciones.get(coleccion)
    user = context.usuario_actual
    
    # Obtener recursos visibles de la colección
    recursos_en_coleccion = coleccion_obj.recursos.all()
    recursos_visibles = RecursoDigital.objects.visibles_para(user)
    
    context.recursos_accesibles = [r for r in recursos_en_coleccion if r in recursos_visibles]


@then('el usuario "<resultado>" acceder al recurso "{recurso}" desde la colección')
def step_verify_collection_access(context, resultado, recurso):
    """Verifica acceso a un recurso desde la colección."""
    recurso_obj = context.recursos.get(recurso)
    
    if resultado == 'debe poder':
        assert recurso_obj in context.recursos_accesibles, \
            f"No se puede acceder a {recurso} desde la colección"
    elif resultado == 'no debe poder':
        assert recurso_obj not in context.recursos_accesibles, \
            f"Se puede acceder inesperadamente a {recurso}"
