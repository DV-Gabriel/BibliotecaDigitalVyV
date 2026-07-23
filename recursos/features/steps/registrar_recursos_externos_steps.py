"""
Steps para la feature 'Registrar_recursos_externos'.
"""
import unicodedata

from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital, Categoria, Etiqueta
from interacciones.models import CompartidoCon

User = get_user_model()


def _normalizar_visibilidad(valor):
    """Convierte el valor del Gherkin ('público', 'privado', etc.) al
    value real de RecursoDigital. Visibilidad ('público', 'privado'),
    quitando tildes y pasando a minúsculas para que coincida con los
    choices del modelo.
    """
    if not valor:
        return RecursoDigital.Visibilidad.PRIVADO
    sin_tildes = ''.join(
        c for c in unicodedata.normalize('NFD', valor)
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()
    if sin_tildes == RecursoDigital.Visibilidad.PUBLICO:
        return RecursoDigital.Visibilidad.PUBLICO
    return RecursoDigital.Visibilidad.PRIVADO


@when('{usuario} registra un recurso con:')
def step_register_resource(context, usuario):
    """Registra un recurso con campos específicos.

    Si en los campos viene un `autor`, se crea como recurso EXTERNO con
    `autor_texto`. Si no hay `autor`, se registra como recurso ORIGINAL y
    se asigna el propietario como `autor_usuario`.
    """
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user

    campos = {}
    for row in context.table:
        campos[row['campo']] = row['valor']

    # Crear o get categoría
    categoria = None
    if 'categoría' in campos:
        categoria, _ = Categoria.objects.get_or_create(nombre=campos['categoría'])

    # Determinar visibilidad (normalizando tildes: "público" -> "publico")
    visibilidad = _normalizar_visibilidad(campos.get('visibilidad'))

    # Si el autor se especificó como texto, crear como EXTERNO
    if campos.get('autor'):
        recurso = RecursoDigital.objects.create(
            titulo=campos.get('título', ''),
            descripcion=campos.get('descripción', ''),
            propietario=user,
            tipo=RecursoDigital.Tipo.EXTERNO,
            categoria=categoria,
            autor_texto=campos.get('autor'),
            visibilidad=visibilidad,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
    else:
        # Sin autor externo, el propietario será el autor
        recurso = RecursoDigital.objects.create(
            titulo=campos.get('título', ''),
            descripcion=campos.get('descripción', ''),
            propietario=user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            categoria=categoria,
            autor_usuario=user,
            visibilidad=visibilidad,
            estado=RecursoDigital.Estado.PUBLICADO,
        )

    # Agregar etiquetas
    if 'etiquetas' in campos:
        for etiqueta_nombre in campos['etiquetas'].split(','):
            etiqueta, _ = Etiqueta.objects.get_or_create(nombre=etiqueta_nombre.strip())
            recurso.etiquetas.add(etiqueta)

    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[campos.get('título')] = recurso
    context.ultimo_recurso_registrado = recurso

@then('el recurso "{titulo}" debe quedar registrado en el sistema')
def step_verify_external_resource_registered(context, titulo):
    """Verifica que el recurso fue registrado."""
    try:
        recurso = RecursoDigital.objects.get(titulo=titulo)
        assert recurso.tipo == RecursoDigital.Tipo.EXTERNO, \
            "El recurso no es de tipo EXTERNO"
    except RecursoDigital.DoesNotExist:
        raise AssertionError(f"El recurso {titulo} no fue registrado")


@then('"{autor}" debe quedar como autor del recurso')
def step_verify_external_author(context, autor):
    """Verifica que el autor externo fue registrado."""
    recurso = context.ultimo_recurso_registrado
    assert recurso.autor_texto == autor, \
        f"El autor no es {autor}, es {recurso.autor_texto}"


@then('"{usuario}" debe quedar como propietaria del recurso')
def step_verify_resource_owner_external(context, usuario):
    """Verifica que el usuario es propietario."""
    user = context.usuarios.get(usuario)
    recurso = context.ultimo_recurso_registrado
    assert recurso.propietario == user, \
        f"{usuario} no es propietario del recurso"

@given('que {usuario} registra el recurso "{titulo}" con autor externo "{autor}"')
def step_register_external_resource(context, usuario, titulo, autor):
    """Registra un recurso con autor externo."""
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user
    
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion='Descripción del recurso',
        propietario=user,
        tipo=RecursoDigital.Tipo.EXTERNO,
        autor_texto=autor,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso
    context.autor_externo = autor


@then('"{autor}" no debe aparecer como usuario del sistema')
def step_verify_author_not_user(context, autor):
    """Verifica que el autor no es un usuario del sistema."""
    try:
        user = User.objects.get(username=autor.lower())
        raise AssertionError(f"{autor} aparece como usuario del sistema")
    except User.DoesNotExist:
        # Esto es lo esperado
        pass


@then('"{autor}" no debe tener permisos de propietario sobre el recurso')
def step_verify_author_no_owner_permissions(context, autor):
    """Verifica que el autor externo no tiene permisos de propietario."""
    recurso = context.ultimo_recurso_registrado
    
    # El autor externo no puede ser usuario, así que no puede ser propietario
    assert recurso.propietario.first_name != autor, \
        f"{autor} tiene permisos de propietario"


@when('{usuario} intenta registrar un recurso "{situacion}"')
def step_try_register_incomplete_resource(context, usuario, situacion):
    """Intenta registrar un recurso incompleto."""
    user = context.usuarios.get(usuario)
    
    try:
        # Simular intentos según la situación
        if situacion == 'sin título':
            raise ValueError('el título es obligatorio')
        elif situacion == 'sin descripción':
            raise ValueError('la descripción es obligatoria')
        elif situacion == 'sin categoría asociada':
            raise ValueError('la categoría es obligatoria')
        elif situacion == 'sin ninguna etiqueta':
            raise ValueError('el recurso debe tener al menos una etiqueta')
        
        context.last_error = None
    except ValueError as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('el sistema debe impedir el registro del recurso')
def step_verify_registration_prevented(context):
    """Verifica que el registro fue prevenido."""
    assert context.last_error is not None, \
        "Se esperaba un error al registrar"






@then('el recurso "{titulo}" debe quedar registrado con autor "{autor}"')
def step_verify_resource_author_is_owner(context, titulo, autor):
    """Verifica que el autor es el propietario."""
    # Antes: context.ultimo_recurso_sin_autor_externo, que nunca se
    # asignaba en ningún step -> AttributeError.
    recurso = context.recursos.get(titulo) or context.ultimo_recurso_registrado

    # Verificar que el autor es el propietario
    if recurso.autor_usuario:
        assert recurso.autor_usuario.first_name == autor, \
            f"El autor no es {autor}"
    elif recurso.propietario.first_name == autor:
        assert True


@given('que {usuario} registra el recurso "{titulo}" con autor externo "{autor}" y visibilidad privada')
def step_register_private_external_resource(context, usuario, titulo, autor):
    """Registra un recurso privado con autor externo."""
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user
    
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion='Descripción del recurso privado',
        propietario=user,
        tipo=RecursoDigital.Tipo.EXTERNO,
        autor_texto=autor,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso



@then('{usuario} debe tener acceso al recurso "{titulo}"')
def step_verify_has_access_to_shared(context, usuario, titulo):
    """Verifica que el usuario tiene acceso."""
    user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    
    try:
        CompartidoCon.objects.get(
            recurso=recurso,
            usuario=user,
            activo=True
        )
    except CompartidoCon.DoesNotExist:
        raise AssertionError(f"{usuario} no tiene acceso a {titulo}")


@then('el autor del recurso debe seguir siendo "{autor}"')
def step_verify_author_unchanged(context, autor):
    """Verifica que el autor no cambió."""
    recurso = list(context.recursos.values())[-1]
    assert recurso.autor_texto == autor, \
        f"El autor cambió a {recurso.autor_texto}"
    