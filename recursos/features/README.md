# Steps BDD para Biblioteca Digital

Este directorio contiene la implementación de todos los pasos (steps) para las features de comportamiento (BDD) de la Biblioteca Digital usando Behave con Django.

## Estructura

```
recursos/features/
├── steps/                                  # Steps (definiciones)
│   ├── __init__.py
│   ├── conftest.py                        # Fixtures y configuración comunes
│   ├── common_steps.py                    # Steps generales (usuarios, etc.)
│   ├── acceder_recursos_steps.py          # Feature: Acceder a recursos
│   ├── compartir_recursos_steps.py        # Feature: Compartir recursos
│   ├── guardar_borrador_steps.py          # Feature: Guardar borrador
│   ├── editar_recursos_propios_steps.py   # Feature: Editar recursos
│   ├── administrar_anotaciones_steps.py   # Feature: Anotaciones
│   ├── gestionar_favoritos_steps.py       # Feature: Favoritos
│   ├── crear_recursos_steps.py            # Feature: Crear recursos
│   ├── organizar_recursos_steps.py        # Feature: Organizar en colecciones
│   └── registrar_recursos_externos_steps.py # Feature: Recursos externos
├── environment.py                         # Configuración de ambiente (Behave)
├── *.feature                              # Archivos de features (Gherkin)
└── README.md                              # Este archivo
```

## Características Cubiertas

### 1. **Acceder_recursos.feature**
- Ver lista de recursos compartidos
- Abrir y consultar contenido
- Control de acceso a recursos privados
- Acceso a recursos públicos

### 2. **Administrar_anotaciones.feature**
- Crear notas personales sobre recursos
- Editar y eliminar anotaciones
- Privacidad garantizada de anotaciones
- Comportamiento con acceso revocado

### 3. **Compartir_recursos.feature**
- Compartir con uno o múltiples usuarios
- Revocar acceso
- Control de duplicación de acceso
- Restricciones por propietario

### 4. **Crear_recursos.feature**
- Detección de similitud de contenido
- Advertencias por contenido similar
- Opción de continuar o cancelar

### 5. **Editar_recursos_propios.feature**
- Modificar título y descripción
- Cambiar categoría
- Actualizar etiquetas
- Modificar autor
- Validación de campos obligatorios

### 6. **Gestionar_favoritos.feature**
- Marcar como favorito según acceso
- Actualización dinámica de acceso
- Pérdida de disponibilidad al revocar

### 7. **Guardar_borrador.feature**
- Guardar borrador incompleto
- Reanudar edición
- Visibilidad solo para propietario
- Publicar al completar campos
- Validación antes de publicar

### 8. **Organizar_recursos.feature**
- Crear colecciones personales
- Agregar recursos según acceso
- Mantener propietario original
- Actualización dinámica de acceso

### 9. **Registrar_recursos_externos.feature**
- Registrar con autor externo
- Autor como texto (no usuario)
- Validación de campos
- Compartir posterior

## Cómo Ejecutar

### Instalar dependencias

```bash
pip install behave django
```

### Ejecutar todos los tests

```bash
behave recursos/features/
```

### Ejecutar una feature específica

```bash
behave recursos/features/compartir_recursos.feature
```

### Ejecutar un escenario específico

```bash
behave recursos/features/compartir_recursos.feature -n "El propietario comparte"
```

### Con más verbosidad

```bash
behave --verbose recursos/features/
```

### Generar reporte

```bash
behave --tags=@importante --format=json recursos/features/ > reporte.json
```

## Estructura de un Step

Los steps siguen la estructura Gherkin: Given (Dado), When (Cuando), Then (Entonces)

### Ejemplo de Step

```python
from behave import given, when, then

@given('que existen los usuarios "{nombres}"')
def step_create_users(context, nombres):
    """Crea múltiples usuarios."""
    # Implementación
    pass

@when('{usuario} comparte "{recurso}" con {receptor}')
def step_share_resource(context, usuario, recurso, receptor):
    """Un usuario comparte un recurso."""
    # Implementación
    pass

@then('el recurso debe aparecer en favoritos')
def step_verify_in_favorites(context):
    """Verifica que el recurso está en favoritos."""
    # Implementación
    pass
```

## Contexto y Estado

El objeto `context` en Behave mantiene el estado durante los tests:

```python
# Guardar datos
context.usuarios = {}
context.recursos = {}
context.usuario_actual = user
context.last_error = None

# Recuperar datos
usuario = context.usuarios.get('Ana')
recurso = context.recursos.get('Álgebra')
```

## Hooks de Ambiente (environment.py)

El archivo `environment.py` proporciona:

- **before_all**: Configuración inicial (Django setup)
- **after_all**: Limpieza final
- **before_scenario**: Preparación de cada escenario
- **after_scenario**: Limpieza de escenario
- **before_step/after_step**: Control por paso individual

## Modelos Utilizados

Los steps utilizan los siguientes modelos Django:

- `usuarios.models.Usuario` - Usuarios del sistema
- `recursos_digitales.models.RecursoDigital` - Recursos educativos
- `recursos_digitales.models.Categoria` - Categorías
- `recursos_digitales.models.Etiqueta` - Etiquetas
- `espacio_personal.models.Coleccion` - Colecciones personales
- `espacio_personal.models.Favorito` - Marcadores favoritos
- `espacio_personal.models.Anotacion` - Notas personales
- `interacciones.models.CompartidoCon` - Control de compartición

## Notas Importantes

1. **Contexto de Usuario**: Muchos steps mantienen un usuario actual en `context.usuario_actual`
2. **Registros**: Los recursos y usuarios se guardan en `context.recursos` y `context.usuarios`
3. **Errores**: Los errores se capturan en `context.last_error` y `context.last_error_message`
4. **Base de Datos**: El ambiente crea una base de datos de prueba limpia
5. **Aislamiento**: Cada escenario es independiente gracias al setup/teardown

## Extensión

Para agregar nuevos steps:

1. Crea un nuevo archivo `nueva_feature_steps.py` en `recursos/features/steps/`
2. Importa decoradores de behave: `from behave import given, when, then`
3. Define funciones con decoradores correspondientes
4. Behave automáticamente descubrirá los nuevos steps

## Debugging

Para debugging, puedes usar:

```python
print(context.usuarios)  # Ver usuarios creados
print(context.last_error_message)  # Ver último error
context.pdb()  # Pausar ejecución
```

O ejecutar con más detalles:

```bash
behave --pdb recursos/features/
```

## Reglas de Negocio Implementadas

Los steps implementan las siguientes reglas clave:

- **RN1**: Campos obligatorios para publicar
- **RN2**: Autor puede no ser usuario del sistema
- **RN3**: Propietario siempre definido
- **RN4**: Compartición y revocación de acceso
- **RN5**: Visibilidad de recursos
- **RN6**: No modificación al organizar
- **RN8**: Privacidad de anotaciones
- **RN9**: Detección de similitud
- **RN10**: Acceso dinámico en favoritos
- **RN12**: Borradores ocultos

---

*Última actualización: 2026-07-16*
