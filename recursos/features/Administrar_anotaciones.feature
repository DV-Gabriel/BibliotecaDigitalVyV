# language: es
Característica: Administrar anotaciones y notas personales por recurso
  Como usuario
  Quiero registrar anotaciones personales sobre los recursos educativos
  Para guardar información importante relacionada con mi aprendizaje

  Antecedentes:
    Dado que soy un usuario autenticado en el sistema
    Y tengo acceso al recurso sobre el cual quiero anotar

  Esquema del escenario: Crear una anotación personal según el tipo de acceso al recurso
    Dado que tengo acceso "<tipo_acceso>" al recurso "<recurso>"
    Cuando agrego una anotación personal sobre "<recurso>"
    Entonces la anotación queda guardada asociada únicamente a mi usuario
    Y no es visible para ningún otro usuario que consulte "<recurso>"

    Ejemplos:
      | tipo_acceso | recurso |
      | propio      | R1      |
      | público     | R2      |
      | compartido  | R3      |

  Escenario: Editar una anotación propia
    Dado que tengo una anotación previa sobre el recurso "R1"
    Cuando modifico el contenido de esa anotación
    Entonces se guarda el nuevo contenido
    Y se conserva su carácter privado

  Escenario: Eliminar una anotación propia
    Dado que tengo una anotación registrada sobre el recurso "R1"
    Cuando elimino dicha anotación
    Entonces la anotación deja de estar asociada al recurso
    Y ya no aparece en mi listado de notas de "R1"

  Escenario: Consultar mis anotaciones sobre un recurso
    Dado que he creado una o más anotaciones sobre el recurso "R1"
    Cuando abro la vista de anotaciones de "R1"
    Entonces veo únicamente las anotaciones que yo mismo he creado

  Escenario: Otro usuario no puede ver mis anotaciones en un recurso compartido
    Dado que comparto el recurso "R1" con otro usuario
    Y yo tengo anotaciones personales sobre "R1"
    Cuando el otro usuario abre "R1"
    Entonces no visualiza ninguna de mis anotaciones

  Escenario: Intentar anotar un recurso al que perdí el acceso
    Dado que el acceso al recurso "R3" me fue revocado por su propietario
    Cuando intento agregar una anotación sobre "R3"
    Entonces el sistema rechaza la acción
    Y me indica que ya no tengo acceso al recurso

  Escenario: Las anotaciones existentes permanecen ocultas tras revocar el acceso
    Dado que tenía anotaciones sobre el recurso "R3"
    Y el propietario revoca mi acceso a "R3"
    Cuando intento consultar mis anotaciones previas de "R3"
    Entonces el sistema no me permite visualizarlas mientras no tenga acceso al recurso

  Esquema del escenario: Visibilidad de anotaciones según el tipo de usuario que consulta el recurso
    Dado que el usuario "<usuario_creador>" crea una anotación sobre un recurso
    Cuando el usuario "<usuario_consultor>" abre ese mismo recurso
    Entonces la anotación es "<visibilidad>"

    Ejemplos:
      | usuario_creador | usuario_consultor             | visibilidad |
      | propietario     | propietario (él mismo)        | visible     |
      | propietario     | usuario con acceso compartido | no visible  |
      | invitado        | propietario del recurso       | no visible  |
      | invitado        | invitado (él mismo)           | visible     |
      | invitado        | otro invitado con acceso      | no visible  |