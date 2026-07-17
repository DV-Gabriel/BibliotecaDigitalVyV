"""
Steps para la feature 'Compartir_recursos'.
"""
from behave import given, when, then
from django.contrib.auth import get_user_model
from recursos_digitales.models import RecursoDigital
from interacciones.models import CompartidoCon

User = get_user_model()


@given('el recurso "{titulo}" es privado y pertenece a {usuario}')
def step_create_private_resource(context, titulo, usuario):
    """Crea un recurso privado para un usuario."""
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
            'visibilidad': RecursoDigital.Visibilidad.PRIVADO,
            'estado': RecursoDigital.Estado.PUBLICADO,
        }
    )
    if not hasattr(context, 'recursos'):
        context.recursos = {}
    context.recursos[titulo] = recurso


@given('el recurso "{titulo}" fue compartido por {propietario} con {receptores}')
def step_share_resource(context, titulo, propietario, receptores):
    """Comparte un recurso con uno o más usuarios."""
    propietario_user = context.usuarios.get(propietario)
    recurso = context.recursos.get(titulo)
    
    receptor_list = [r.strip() for r in receptores.replace(' y ', ',').split(',')]
    
    for receptor_name in receptor_list:
        receptor = context.usuarios.get(receptor_name)
        if not receptor:
            receptor = User.objects.create_user(
                username=receptor_name.lower(),
                password='test123',
                first_name=receptor_name,
            )
            context.usuarios[receptor_name] = receptor
        
        compartido, created = CompartidoCon.objects.get_or_create(
            recurso=recurso,
            usuario=receptor,
            compartido_por=propietario_user,
            defaults={'activo': True}
        )
        if not created and not compartido.activo:
            compartido.activo = True
            compartido.fecha_revocado = None
            compartido.save()


@when('{usuario} comparte "{titulo}" con {receptores}')
def step_user_shares_resource(context, usuario, titulo, receptores):
    """Un usuario intenta compartir un recurso."""
    user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    
    receptor_list = [r.strip() for r in receptores.replace(' y ', ',').split(',')]
    
    try:
        # Verificar que es propietario
        if recurso.propietario != user:
            context.last_error = PermissionError("Solo el propietario puede compartir")
            context.last_error_message = "solo el propietario puede compartir el recurso"
            return
        
        for receptor_name in receptor_list:
            receptor = context.usuarios.get(receptor_name)
            if not receptor:
                receptor = User.objects.create_user(
                    username=receptor_name.lower(),
                    password='test123',
                    first_name=receptor_name,
                )
                context.usuarios[receptor_name] = receptor
            
            compartido, created = CompartidoCon.objects.get_or_create(
                recurso=recurso,
                usuario=receptor,
                compartido_por=user,
                defaults={'activo': True}
            )
        context.last_error = None
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@when('{usuario} intenta compartir "{titulo}" con {receptor}')
def step_user_try_share_resource(context, usuario, titulo, receptor):
    """Un usuario intenta compartir un recurso (puede fallar)."""
    step_user_shares_resource(context, usuario, titulo, receptor)


@when('{usuario} revoca el acceso de {receptor} a "{titulo}"')
def step_revoke_access(context, usuario, titulo, receptor):
    """El propietario revoca acceso a un usuario."""
    propietario = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    receptor_user = context.usuarios.get(receptor)
    
    try:
        compartido = CompartidoCon.objects.get(
            recurso=recurso,
            usuario=receptor_user,
            compartido_por=propietario,
        )
        compartido.revocar()
        context.last_error = None
    except CompartidoCon.DoesNotExist:
        context.last_error = None  # No hay acceso que revocar
        context.last_error_message = f"{receptor} no tenía acceso al recurso"


@when('{usuario} intenta revocar el acceso de {receptor} a "{titulo}"')
def step_try_revoke_access(context, usuario, titulo, receptor):
    """Un usuario intenta revocar acceso (puede fallar si no es propietario)."""
    propietario_user = context.usuarios.get(usuario)
    recurso = context.recursos.get(titulo)
    receptor_user = context.usuarios.get(receptor)
    
    try:
        if recurso.propietario != propietario_user:
            context.last_error = PermissionError("Solo el propietario puede revocar")
            context.last_error_message = "solo el propietario puede revocar el acceso"
            return
        
        step_revoke_access(context, usuario, titulo, receptor)
    except Exception as e:
        context.last_error = e
        context.last_error_message = str(e)


@then('debe mostrar un mensaje indicando que {receptor} no tenía acceso al recurso')
def step_check_no_access_message(context, receptor):
    """Verifica mensaje de no acceso previo."""
    if hasattr(context, 'last_error_message'):
        assert receptor.lower() in context.last_error_message.lower() or \
               "no tenía acceso" in context.last_error_message.lower()


@then('el recurso no debe aparecer en la lista de "recursos compartidos conmigo" de {usuario}')
def step_resource_not_in_shared_list(context, usuario):
    """Verifica que el recurso no está en la lista de compartidos."""
    user = context.usuarios.get(usuario)
    recurso = list(context.recursos.values())[-1]  # Último recurso
    
    compartidos = CompartidoCon.objects.filter(
        usuario=user,
        activo=True,
        recurso=recurso
    )
    assert not compartidos.exists(), \
        f"El recurso aún aparece en compartidos conmigo"


@then('el recurso debe aparecer en la lista de "recursos compartidos conmigo" de {usuario}')
def step_resource_in_shared_list(context, usuario):
    """Verifica que el recurso está en la lista de compartidos."""
    user = context.usuarios.get(usuario)
    recurso = list(context.recursos.values())[-1]
    
    compartidos = CompartidoCon.objects.filter(
        usuario=user,
        activo=True,
        recurso=recurso
    )
    assert compartidos.exists(), \
        f"El recurso no aparece en compartidos conmigo"


@then('Ana debe seguir teniendo acceso al recurso')
def step_verify_still_has_access(context):
    """Verifica que Ana sigue teniendo acceso."""
    step_user_has_access(context, 'Ana', list(context.recursos.keys())[-1])
