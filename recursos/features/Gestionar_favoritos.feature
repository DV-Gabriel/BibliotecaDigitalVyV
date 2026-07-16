# language: es

  # Se retiró: marcar como favorito exitosamente por tipo de recurso público/propio
  # (es solo confirmación de una acción CRUD sin condición de negocio), evitar duplicado
  # de favorito, quitar de favoritos, visualizar lista ordenada por fecha, y acceso rápido/redirección
  # — todo eso es CRUD y UI, no regla de negocio.
  #
  #Se conserva únicamente lo que depende de RN5/RN10: qué se puede marcar como favorito según
  # el acceso al recurso, y qué pasa con un favorito cuando cambia el acceso al recurso original.

  #Nota: crear/eliminar un favorito, evitar duplicados en la lista, ordenarla por fecha y el acceso
  # rápido (clic → redirección) son funcionalidad de producto legítima, pero de sistema/UI, no de
  # negocio — se recomienda documentarlas como historias de usuario técnicas o casos de prueba de
  # interfaz, no como escenarios BDD de negocio.

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