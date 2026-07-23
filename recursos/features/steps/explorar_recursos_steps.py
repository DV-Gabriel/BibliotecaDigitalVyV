"""Steps de exploración del catálogo y metadatos de autoría."""
from behave import given, when, then
from django.contrib.auth import get_user_model

from interacciones.models import CompartidoCon
from recursos_digitales.models import RecursoDigital


User = get_user_model()


def _usuario(context, nombre, rol=None):
    usuario, _ = User.objects.get_or_create(
        username=nombre.lower().replace(' ', '_'),
        defaults={'first_name': nombre, 'rol': rol or User.Rol.ESTUDIANTE},
    )
    if rol and usuario.rol != rol:
        usuario.rol = rol
        usuario.save(update_fields=['rol'])
    context.usuarios[nombre] = usuario
    return usuario


@given('que existen los siguientes recursos en el sistema:')
def step_catalog_resources(context):
    for row in context.table:
        propietario = _usuario(context, row['propietario'])
        visibilidad = (
            RecursoDigital.Visibilidad.PUBLICO
            if row['visibilidad'] == 'publico'
            else RecursoDigital.Visibilidad.PRIVADO
        )
        recurso = RecursoDigital.objects.create(
            titulo=row['titulo'],
            descripcion=f"Descripción de {row['titulo']}",
            propietario=propietario,
            autor_usuario=propietario,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=visibilidad,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
        context.recursos[row['titulo']] = recurso


@when('{usuario} busca "{texto}" en el catálogo')
def step_search_catalog(context, usuario, texto):
    user = _usuario(context, usuario)
    context.resultados_busqueda = RecursoDigital.objects.visibles_para(user).filter(
        titulo__icontains=texto
    )


@then('debe ver el recurso "{titulo}" en los resultados')
def step_resource_in_results(context, titulo):
    assert context.resultados_busqueda.filter(titulo=titulo).exists()


@then('no debe ver el recurso "{titulo}" en los resultados')
def step_resource_not_in_results(context, titulo):
    assert not context.resultados_busqueda.filter(titulo=titulo).exists()


@given('que el recurso "{titulo}" fue compartido por {propietario} con {receptor}')
def step_catalog_shared_resource(context, titulo, propietario, receptor):
    owner = _usuario(context, propietario)
    recipient = _usuario(context, receptor)
    recurso = context.recursos.get(titulo)
    if recurso is None:
        recurso = RecursoDigital.objects.create(
            titulo=titulo,
            descripcion=f'Descripción de {titulo}',
            propietario=owner,
            autor_usuario=owner,
            tipo=RecursoDigital.Tipo.ORIGINAL,
            visibilidad=RecursoDigital.Visibilidad.PRIVADO,
            estado=RecursoDigital.Estado.PUBLICADO,
        )
        context.recursos[titulo] = recurso
    CompartidoCon.objects.update_or_create(
        recurso=recurso,
        usuario=recipient,
        defaults={'compartido_por': owner, 'activo': True},
    )


@given('que el recurso "{titulo}" tiene como autor a un usuario con rol "{rol}"')
def step_resource_author_role(context, titulo, rol):
    autor = _usuario(context, f'autor_{rol}', rol=rol)
    recurso = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion=f'Descripción de {titulo}',
        propietario=autor,
        autor_usuario=autor,
        tipo=RecursoDigital.Tipo.ORIGINAL,
        visibilidad=RecursoDigital.Visibilidad.PUBLICO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )
    context.recursos[titulo] = recurso


@given('que el recurso "{titulo}" tiene como autor externo a "{autor}"')
def step_external_author(context, titulo, autor):
    owner = _usuario(context, 'Ana')
    context.recursos[titulo] = RecursoDigital.objects.create(
        titulo=titulo,
        descripcion=f'Descripción de {titulo}',
        propietario=owner,
        autor_texto=autor,
        tipo=RecursoDigital.Tipo.EXTERNO,
        visibilidad=RecursoDigital.Visibilidad.PUBLICO,
        estado=RecursoDigital.Estado.PUBLICADO,
    )


@when('{usuario} consulta el recurso "{titulo}"')
def step_consult_resource(context, usuario, titulo):
    context.recurso_consultado = context.recursos[titulo]


@then('debe ver que el autor tiene el rol "{rol}"')
def step_verify_author_role(context, rol):
    assert context.recurso_consultado.autor_usuario.rol == rol


@then('el sistema no debe mostrar ningún rol asociado al autor')
def step_verify_external_has_no_role(context):
    assert context.recurso_consultado.autor_usuario is None
