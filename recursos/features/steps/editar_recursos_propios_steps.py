"""
Steps para la feature 'Editar_recursos_propios'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital, Categoria, Etiqueta

User = get_user_model()


@given('existen los usuarios "{nombres}"')
def step_create_users_from_list(context, nombres):
    """Crea usuarios a partir de una lista."""
    user_list = [n.strip() for n in nombres.split(',')]
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


@given('{usuario} ha creado el recurso "{titulo}" con:')
def step_create_resource_with_fields(context, usuario, titulo):
    """Crea un recurso con campos específicos."""
    user = context.usuarios.get(usuario)
    
    campos = {}
    for row in context.table:
        campos[row['campo']] = row['valor']
    
    # Crear o actualizar categoría
    categoria = None
    if 'categoría' in campos:
        categoria, _ = Categoria.objects.get_or_create(nombre=campos['categoría'])
    
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion=campos.get('descripción', ''),
        propietario=user,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PRIVADO,
        estado=RecursoDigital.Estado.PUBLICADO,
        categoria=categoria,
    )
    
    # Agregar etiquetas
    if 'etiquetas' in campos:
        for etiqueta_nombre in campos['etiquetas'].split(','):
            etiqueta, _ = Etiqueta.objects.get_or_create(nombre=etiqueta_nombre.strip())
            recurso.etiquetas.add(etiqueta)
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@when('el usuario modifica el título del recurso a "{nuevo_titulo}"')
def step_modify_title(context, nuevo_titulo):
    """Modifica el título del recurso."""
    recurso = list(context.recursos.values())[-1]
    recurso.titulo = nuevo_titulo
    recurso.save()
    context.titulo_modificado = nuevo_titulo


@then('el recurso debe actualizarse con el nuevo título y descripción')
def step_verify_title_description_updated(context):
    """Verifica que título y descripción fueron actualizados."""
    recurso = list(context.recursos.values())[-1]
    recurso.refresh_from_db()
    
    assert recurso.titulo == context.titulo_modificado, "Título no actualizado"
    if hasattr(context, 'descripcion_modificada'):
        assert recurso.descripcion == context.descripcion_modificada, \
            "Descripción no actualizada"


@when('modifica la descripción a "{nueva_descripcion}"')
def step_modify_description(context, nueva_descripcion):
    """Modifica la descripción."""
    recurso = list(context.recursos.values())[-1]
    recurso.descripcion = nueva_descripcion
    recurso.save()
    context.descripcion_modificada = nueva_descripcion


@then('{usuario} debe seguir siendo el propietario del recurso')
def step_verify_owner_unchanged(context, usuario):
    """Verifica que el propietario no cambió."""
    recurso = list(context.recursos.values())[-1]
    user = context.usuarios.get(usuario)
    assert recurso.propietario == user, "El propietario cambió inesperadamente"


@when('el usuario cambia la categoría del recurso a "{nueva_categoria}"')
def step_change_category(context, nueva_categoria):
    """Cambia la categoría del recurso."""
    recurso = list(context.recursos.values())[-1]
    categoria, _ = Categoria.objects.get_or_create(nombre=nueva_categoria)
    recurso.categoria = categoria
    recurso.save()
    context.categoria_modificada = nueva_categoria


@then('el recurso debe mostrar la nueva categoría "{categoria}"')
def step_verify_category_updated(context, categoria):
    """Verifica que la categoría fue actualizada."""
    recurso = list(context.recursos.values())[-1]
    recurso.refresh_from_db()
    assert recurso.categoria.nombre == categoria, \
        f"Categoría no es {categoria}, es {recurso.categoria.nombre}"


@when('el usuario agrega la etiqueta "{etiqueta}" al recurso')
def step_add_tag(context, etiqueta):
    """Agrega una etiqueta."""
    recurso = list(context.recursos.values())[-1]
    etiqueta_obj, _ = Etiqueta.objects.get_or_create(nombre=etiqueta)
    recurso.etiquetas.add(etiqueta_obj)
    context.etiqueta_agregada = etiqueta


@when('quita la etiqueta "{etiqueta}"')
def step_remove_tag(context, etiqueta):
    """Quita una etiqueta."""
    recurso = list(context.recursos.values())[-1]
    try:
        etiqueta_obj = Etiqueta.objects.get(nombre=etiqueta)
        recurso.etiquetas.remove(etiqueta_obj)
        context.etiqueta_eliminada = etiqueta
    except Etiqueta.DoesNotExist:
        pass


@then('el recurso debe tener las etiquetas "{etiquetas}"')
def step_verify_tags(context, etiquetas):
    """Verifica que el recurso tiene las etiquetas esperadas."""
    recurso = list(context.recursos.values())[-1]
    recurso.refresh_from_db()
    
    nombres_etiquetas = [e.nombre for e in recurso.etiquetas.all()]
    etiquetas_esperadas = [e.strip() for e in etiquetas.split(' y ')]
    
    for etiqueta in etiquetas_esperadas:
        assert etiqueta in nombres_etiquetas, \
            f"Etiqueta {etiqueta} no encontrada. Etiquetas actuales: {nombres_etiquetas}"


@when('el usuario modifica el autor del recurso a "{nuevo_autor}"')
def step_modify_author(context, nuevo_autor):
    """Modifica el autor del recurso."""
    recurso = list(context.recursos.values())[-1]
    recurso.autor_texto = nuevo_autor
    recurso.save()
    context.autor_modificado = nuevo_autor


@then('el recurso debe mostrar el nuevo autor "{autor}"')
def step_verify_author_updated(context, autor):
    """Verifica que el autor fue actualizado."""
    recurso = list(context.recursos.values())[-1]
    recurso.refresh_from_db()
    assert recurso.autor_texto == autor, \
        f"Autor no es {autor}, es {recurso.autor_texto}"


@given('que "{usuario}" ha creado el recurso "{titulo}"')
def step_ensure_user_created_resource(context, usuario, titulo):
    """Asegura que un usuario creó un recurso."""
    user = context.usuarios.get(usuario)
    try:
        recurso = RecursoDigital.objects.get(titulo=titulo)
    except RecursoDigital.DoesNotExist:
        recurso = RecursoDigital.objects.create(
            titulo=titulo,
            descripcion='Descripción',
            propietario=user,
            tipo=RecursoDigital.Tipo.ORIGINAL,
        )
    
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso



@when('el usuario intenta "{accion}" del recurso "{titulo}"')
def step_user_try_action(context, accion, titulo):
    """Un usuario intenta una acción específica."""
    recurso = list(context.recursos.values())[-1]
    
    try:
        if accion == "borrar el título":
            recurso.titulo = ''
            context.accion_intento = "borrar el título"
        elif accion == "borrar la descripción":
            recurso.descripcion = ''
            context.accion_intento = "borrar la descripción"
        elif accion == "quitar todas las etiquetas":
            recurso.etiquetas.clear()
            context.accion_intento = "quitar todas las etiquetas"
        elif accion == "desvincular la categoría":
            recurso.categoria = None
            context.accion_intento = "desvincular la categoría"
        
        # Intentar guardar
        recurso.clean()  # Esto debería lanzar ValidationError
        recurso.save()
        context.last_error = None
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('el sistema debe impedir guardar los cambios')
def step_verify_changes_rejected(context):
    """Verifica que los cambios fueron rechazados."""
    assert context.last_error is not None, \
        "Se esperaba un error al guardar"



