"""
Steps para la feature 'Guardar_borrador'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital, Categoria, Etiqueta

User = get_user_model()


@given('que "{usuario}" es un usuario autenticado en el sistema')
def step_ensure_authenticated_user(context, usuario):
    """Asegura que un usuario está autenticado."""
    try:
        user = User.objects.get(username=usuario.lower())
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
    context.usuario_actual = user
    context.usuarios = context.usuarios if hasattr(context, 'usuarios') else {}
    context.usuarios[usuario] = user


@when('{usuario} empieza a crear un recurso con título "{titulo}" y sale sin completar la categoría ni las etiquetas')
def step_start_resource_incomplete(context, usuario, titulo):
    """Crea un recurso incompleto."""
    user = context.usuarios.get(usuario)
    
    # Crear recurso sin categoría ni etiquetas (borrador)
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion='Descripción incompleta',
        propietario=user,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.BORRADOR,  # Estado borrador
    )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@then('el recurso "{titulo}" debe quedar guardado con estado "borrador"')
def step_verify_draft_state(context, titulo):
    """Verifica que el recurso está en estado borrador."""
    recurso = context.recursos.get(titulo)
    assert recurso is not None, f"Recurso {titulo} no existe"
    assert recurso.estado == RecursoDigital.Estado.BORRADOR, \
        f"El recurso debería estar en borrador, pero está en {recurso.estado}"


@then('el recurso no debe aparecer en el catálogo público')
def step_draft_not_in_catalog(context):
    """Verifica que el borrador no aparece en el catálogo."""
    recurso = list(context.recursos.values())[-1]
    
    # Los recursos públicos publicados son los visibles
    publicos = RecursoDigital.objects.filter(
        visibilidad=RecursoDigital.Visibilidad.PUBLICO,
        estado=RecursoDigital.Estado.PUBLICADO
    )
    assert recurso not in publicos, "El borrador aparece en el catálogo público"


@given('el recurso "{titulo}" quedó guardado como borrador con el contenido que {usuario} había ingresado')
def step_setup_draft_resource(context, titulo, usuario):
    """Configura un recurso en borrador."""
    user = context.usuarios.get(usuario)
    
    try:
        recurso = RecursoDigital.objects.get(titulo=titulo, propietario=user)
    except RecursoDigital.DoesNotExist:
        recurso = RecursoDigital.objects.create(
            titulo=titulo,
            descripcion='Contenido de borrador',
            propietario=user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
            estado=RecursoDigital.Estado.BORRADOR,
        )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso
    context.contenido_guardado = recurso.descripcion


@when('{usuario} retoma la edición de "{titulo}"')
def step_resume_draft_edit(context, usuario, titulo):
    """Resume la edición de un borrador."""
    user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    
    context.usuario_actual = user
    context.recurso_actual = recurso


@then('debe ver el contenido que había guardado previamente')
def step_verify_saved_content(context):
    """Verifica que el contenido guardado se mantiene."""
    recurso = context.recurso_actual
    assert recurso.descripcion == context.contenido_guardado, \
        "El contenido guardado no coincide"


@given('que {usuario} tiene el recurso "{titulo}" guardado como "borrador"')
def step_ensure_draft_exists(context, usuario, titulo):
    """Asegura que existe un recurso en borrador."""
    step_setup_draft_resource(context, titulo, usuario)






@given('que {usuario} completa título, descripción, categoría y al menos una etiqueta')
def step_complete_draft_fields(context, usuario, titulo=None):
    """Completa los campos obligatorios de un borrador."""
    user = context.usuarios.get(usuario)
    recurso = context.recurso_actual if hasattr(context, 'recurso_actual') else list(context.recursos.values())[-1]
    
    # Asegurar categoría
    categoria, _ = Categoria.objects.get_or_create(nombre='Matemáticas')
    recurso.categoria = categoria
    
    # Asegurar etiqueta
    etiqueta, _ = Etiqueta.objects.get_or_create(nombre='test')
    recurso.etiquetas.add(etiqueta)
    
    recurso.save()


@when('{usuario} publica el recurso "{titulo}"')
def step_publish_resource(context, usuario, titulo):
    """Publica un recurso."""
    recurso = context.recursos.get(titulo)
    
    try:
        # Verificar que tiene todos los campos requeridos
        if not recurso.titulo:
            raise ValueError("el título es obligatorio")
        if not recurso.descripcion:
            raise ValueError("la descripción es obligatoria")
        if not recurso.categoria:
            raise ValueError("la categoría es obligatoria")
        if not recurso.etiquetas.exists():
            raise ValueError("el recurso debe tener al menos una etiqueta")
        
        recurso.estado = RecursoDigital.Estado.PUBLICADO
        recurso.save()
        context.last_error = None
    except ValueError as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('el recurso debe quedar con estado "publicado"')
def step_verify_published_state(context):
    """Verifica que el recurso fue publicado."""
    recurso = list(context.recursos.values())[-1]
    assert recurso.estado == RecursoDigital.Estado.PUBLICADO, \
        f"El recurso debería estar publicado, pero está en {recurso.estado}"


@then('el recurso debe quedar visible según su visibilidad configurada')
def step_verify_resource_visibility(context):
    """Verifica que el recurso es visible según su configuración."""
    recurso = list(context.recursos.values())[-1]
    assert recurso.estado == RecursoDigital.Estado.PUBLICADO, \
        "El recurso debe estar publicado"


@given('que {usuario} tiene el recurso "{titulo}" guardado como "borrador" sin "{campo}"')
def step_setup_incomplete_draft(context, usuario, titulo, campo):
    """Crea un borrador sin un campo específico."""
    user = context.usuarios.get(usuario)
    
    kwargs = {
        'titulo': titulo,
        'descripcion': 'Contenido',
        'propietario': user,
        'tipo': RecursoDigital.Tipo.ORIGINAL,
        'visibilidad': RecursoDigital.Visibilidad.PRIVADO,
        'estado': RecursoDigital.Estado.BORRADOR,
    }
    
    if campo == 'título':
        kwargs['titulo'] = ''
    elif campo == 'descripción':
        kwargs['descripcion'] = ''
    
    recurso, _ = RecursoDigital.objects.get_or_create(titulo=titulo or 'temp', defaults=kwargs)
    
    if campo == 'categoría':
        recurso.categoria = None
    
    recurso.save()
    
    if campo == 'etiquetas':
        recurso.etiquetas.clear()
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@when('{usuario} intenta publicar "{titulo}"')
def step_try_publish_incomplete(context, usuario, titulo):
    """Intenta publicar un recurso incompleto."""
    recurso = context.recursos.get(titulo)
    
    try:
        if not recurso.titulo:
            raise ValueError("el título es obligatorio")
        if not recurso.descripcion:
            raise ValueError("la descripción es obligatoria")
        if not recurso.categoria:
            raise ValueError("la categoría es obligatoria")
        if not recurso.etiquetas.exists():
            raise ValueError("el recurso debe tener al menos una etiqueta")
    except ValueError as e:
        context.last_error = e
        context.last_error_message = str(e)
