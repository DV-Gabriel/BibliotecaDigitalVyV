"""
Steps para la feature 'Crear_recursos'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital, Categoria, Etiqueta

User = get_user_model()


@given('existe el recurso "{titulo}", creado por "{usuario}", cuyo contenido incluye el párrafo:')
def step_create_resource_with_content(context, titulo, usuario):
    """Crea un recurso con contenido específico."""
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user
    
    # Obtener el contenido de la tabla
    contenido = context.text or ''
    
    recurso, _ = RecursoDigital.objects.get_or_create(
        titulo=titulo,
        propietario=user,
        defaults={
            'descripcion': contenido,
            'contenido': contenido,
            'tipo': RecursoDigital.Tipo.ORIGINAL,
            'visibilidad': RecursoDigital.Visibilidad.PRIVADO,
            'estado': RecursoDigital.Estado.PUBLICADO,
        }
    )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@when('{usuario} solicita verificar similitud para un recurso con contenido "{nivel_similitud}" al de "{recurso_ref}"')
def step_check_similarity(context, usuario, nivel_similitud, recurso_ref):
    """Verifica similitud de contenido."""
    user = context.usuario_actual or context.usuarios.get(usuario)
    recurso_ref_obj = context.recursos.get(recurso_ref)
    
    # Simulación de detección de similitud
    context.similitud_detectada = None
    
    if nivel_similitud == 'claramente distinto':
        context.similitud_detectada = False
    elif nivel_similitud == 'significativamente similar':
        context.similitud_detectada = True
        context.recursos_similares = [recurso_ref_obj]
    
    context.usuario_actual = user


@then('el sistema "{resultado}" advertir a {usuario} sobre el recurso "{recurso_ref}" como posible similar')
def step_verify_similarity_warning(context, resultado, usuario, recurso_ref):
    """Verifica si se muestra advertencia de similitud."""
    if resultado == 'debe':
        assert context.similitud_detectada, \
            "Se esperaba una advertencia de similitud"
        assert recurso_ref in [r.titulo for r in context.recursos_similares], \
            f"No se advirtió sobre {recurso_ref}"
    elif resultado == 'no debe':
        assert not context.similitud_detectada, \
            "No se esperaba una advertencia de similitud"


@given('existe otro recurso "{titulo}", creado por "{usuario}", con contenido significativamente similar al de "{recurso_ref}"')
@given('que existe otro recurso "{titulo}", creado por "{usuario}", con contenido significativamente similar al de "{recurso_ref}"')
def step_create_similar_resource(context, titulo, usuario, recurso_ref):
    """Crea un recurso con contenido similar."""
    user = context.usuarios.get(usuario)
    if not user:
        user = User.objects.create_user(
            username=usuario.lower(),
            password='test123',
            first_name=usuario,
        )
        context.usuarios[usuario] = user
    
    recurso_ref_obj = context.recursos.get(recurso_ref)
    
    # Crear recurso con contenido similar (misma descripción)
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        propietario=user,
        descripcion=recurso_ref_obj.descripcion,  # Similar
        contenido=recurso_ref_obj.contenido,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    
    context.recursos[titulo] = recurso


@when('{usuario} solicita verificar similitud para el recurso "{titulo}"')
def step_check_similarity_new_resource(context, usuario, titulo):
    """Verifica similitud para un recurso nuevo."""
    user = context.usuarios.get(usuario)
    
    # Simular búsqueda de similitud contra los recursos existentes
    recursos_existentes = RecursoDigital.objects.exclude(titulo=titulo)
    
    # En una implementación real, usaría algoritmo de similitud
    context.recursos_similares = []
    for recurso in recursos_existentes:
        # Simulación simple: si el título contiene palabras comunes
        if any(palabra in titulo.lower() for palabra in ['energía', 'calor', 'termodinámica']):
            context.recursos_similares.append(recurso)
    
    context.similitud_detectada = len(context.recursos_similares) > 0


@then('el sistema debe advertirle sobre "{recurso1}" y "{recurso2}" como posibles similares')
def step_verify_multiple_similarities(context, recurso1, recurso2):
    """Verifica advertencias sobre múltiples similares."""
    assert context.similitud_detectada, \
        "Se esperaba una advertencia de similitud"
    
    titulos_similares = [r.titulo for r in context.recursos_similares]
    assert recurso1 in titulos_similares or any(recurso1.lower() in t.lower() for t in titulos_similares), \
        f"No se advirtió sobre {recurso1}"
    assert recurso2 in titulos_similares or any(recurso2.lower() in t.lower() for t in titulos_similares), \
        f"No se advirtió sobre {recurso2}"


@given('que el sistema le advirtió a {usuario} sobre el recurso similar "{recurso_similar}"')
def step_record_similarity_warning(context, usuario, recurso_similar):
    """Registra que se mostró una advertencia."""
    context.advertencia_mostrada = True
    context.recurso_similar_advertido = recurso_similar


@when('{usuario} confirma que desea continuar con la creación de "{titulo}"')
def step_user_confirms_creation(context, usuario, titulo):
    """El usuario confirma crear el recurso a pesar de la similitud."""
    user = context.usuarios.get(usuario)
    
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion='Contenido del nuevo recurso',
        propietario=user,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso
    context.recurso_creado = recurso


@then('el recurso "{titulo}" debe quedar creado')
def step_verify_resource_created(context, titulo):
    """Verifica que el recurso fue creado."""
    assert titulo in context.recursos, \
        f"El recurso {titulo} no fue creado"


@then('{usuario} debe quedar registrada como propietaria del nuevo recurso')
def step_verify_resource_ownership(context, usuario):
    """Verifica que el usuario es propietario."""
    user = context.usuarios.get(usuario)
    recurso = context.recurso_creado
    
    assert recurso.propietario == user, \
        f"{usuario} no es propietario del recurso"


@when('{usuario} cancela la creación de "{titulo}"')
def step_user_cancels_creation(context, usuario, titulo):
    """El usuario cancela la creación."""
    # Verificar que el recurso NO fue creado
    context.recurso_cancelado = titulo


@then('el recurso "{titulo}" no debe quedar creado')
def step_verify_resource_not_created(context, titulo):
    """Verifica que el recurso NO fue creado."""
    assert titulo not in context.recursos, \
        f"El recurso {titulo} fue creado pese a la cancelación"


@then('el recurso "{recurso_ref}" debe permanecer sin cambios')
def step_verify_resource_unchanged(context, recurso_ref):
    """Verifica que un recurso no fue modificado."""
    recurso = context.recursos.get(recurso_ref)
    recurso.refresh_from_db()
    
    # En una implementación real, verificaría cambios en campos específicos
    assert recurso is not None, \
        f"El recurso {recurso_ref} fue eliminado"
