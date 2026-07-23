# language: es

Característica: Crear recursos personalizados originales (detección de similitud por contenido)
  Como usuario
  Quiero que el sistema me advierta si el contenido de mi recurso es significativamente similar a uno existente (RN9)
  Para reutilizar información existente o reestructurar mi recurso y aportar algo distinto

  Antecedentes:
    Dado que "Ana" es un usuario autenticado en el sistema
    Y existe el recurso "Resumen de Termodinámica", creado por "Luis", cuyo contenido incluye el párrafo:
      """
      La termodinámica estudia las relaciones entre el calor, el trabajo y la energía
      en los sistemas físicos, así como sus transformaciones.
      """

  Esquema del escenario: El sistema advierte al usuario según el nivel de similitud del contenido (RN9)
    Cuando Ana solicita verificar similitud para un recurso con contenido "<nivel_similitud>" al de "Resumen de Termodinámica"
    Entonces el sistema "<resultado>" advertir a Ana sobre el recurso "Resumen de Termodinámica" como posible similar

    Ejemplos:
      | nivel_similitud       | resultado    |
      | claramente distinto   | no debe      |
      | significativamente similar | debe    |

  Escenario: El sistema detecta varios recursos significativamente similares y los muestra todos (RN9)
    Dado que existe otro recurso "Guía de Transferencia de Calor", creado por "Marta", con contenido significativamente similar al de "Resumen de Termodinámica"
    Cuando Ana solicita verificar similitud para el recurso "Apuntes de Energía y Calor"
    Entonces el sistema debe advertirle sobre "Resumen de Termodinámica" y "Guía de Transferencia de Calor" como posibles similares

  # --- Decisión del usuario tras ver el recurso similar ---

  Escenario: El usuario decide continuar con la creación pese a la similitud detectada
    Dado que el sistema le advirtió a Ana sobre el recurso similar "Resumen de Termodinámica"
    Cuando Ana confirma que desea continuar con la creación de "Apuntes de Energía y Calor"
    Entonces el recurso "Apuntes de Energía y Calor" debe quedar creado
    Y Ana debe quedar registrada como propietaria del nuevo recurso

  Escenario: El usuario cancela la creación tras ver el recurso similar
    Dado que el sistema le advirtió a Ana sobre el recurso similar "Resumen de Termodinámica"
    Cuando Ana cancela la creación de "Apuntes de Energía y Calor"
    Entonces el recurso "Apuntes de Energía y Calor" no debe quedar creado
    Y el recurso "Resumen de Termodinámica" debe permanecer sin cambios
