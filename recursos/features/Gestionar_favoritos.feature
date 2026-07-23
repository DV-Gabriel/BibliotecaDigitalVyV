# language: es
Característica: Gestionar favoritos y marcadores de acceso rápido
  Como usuario
  Quiero que mis favoritos respeten en todo momento el acceso vigente al recurso original (RN5, RN10)
  Para no perder ni conservar indebidamente acceso a través de un marcador

  Antecedentes:
    Dado que soy un usuario autenticado en el sistema

  Esquema del escenario: Marcar como favorito según el tipo de acceso al recurso (RN5)
    Dado que existe un recurso de tipo "<tipo_recurso>"
    Cuando intento marcarlo como favorito
    Entonces el resultado de la acción es "<resultado>"

    Ejemplos:
      | tipo_recurso                   | resultado             |
      | público                        | marcado exitosamente  |
      | compartido conmigo              | marcado exitosamente  |
      | propio                          | marcado exitosamente  |
      | privado no compartido conmigo   | acción rechazada      |

  Escenario: Un recurso favorito pierde disponibilidad al revocarse el acceso compartido (RN10)
    Dado que el recurso "R2" está en mi lista de favoritos
    Y el propietario revoca el acceso compartido sobre "R2"
    Cuando accedo a mi lista de favoritos
    Entonces "R2" ya no está disponible para abrir
    Y el sistema indica que el acceso fue revocado
