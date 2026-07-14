# language: es
Característica: Crear recursos personalizados originales (detección de similitud por contenido)
  Como estudiante o docente
  Quiero que el sistema detecte si el contenido de mi recurso es similar a uno existente
  Para reutilizar información existente o reestructurar mi recurso y aportar algo distinto

  Antecedentes:
    Dado que "Ana" es un usuario autenticado en el sistema
    Y existe el recurso "Resumen de Termodinámica", creado por "Luis", cuyo contenido incluye el párrafo:
      """
      La termodinámica estudia las relaciones entre el calor, el trabajo y la energía
      en los sistemas físicos, así como sus transformaciones.
      """

  # --- Detección de similitud por contenido ---

  Escenario: El sistema detecta un recurso similar cuando el contenido supera el 70% de similitud
    Cuando Ana solicita verificar similitud para el recurso "Apuntes de Energía y Calor", cuyo contenido tiene un 85% de similitud con "Resumen de Termodinámica"
    Entonces el sistema debe mostrarle el recurso "Resumen de Termodinámica" como posible similar
  Antes de que Ana confirme la creación

  Escenario: El sistema no marca como similar un recurso por debajo del umbral
    Cuando Ana solicita verificar similitud para el recurso "Introducción a la Biología Celular", cuyo contenido tiene un 15% de similitud con "Resumen de Termodinámica"
    Entonces el sistema no debe mostrar ningún recurso similar

  Escenario: El sistema detecta varios recursos que superan el umbral y los muestra todos
    Dado que existe otro recurso "Guía de Transferencia de Calor", creado por "Marta"
    Cuando Ana solicita verificar similitud para el recurso "Apuntes de Energía y Calor":
      | recurso_existente              | porcentaje_similitud |
      | Resumen de Termodinámica       | 85%                  |
      | Guía de Transferencia de Calor | 72%                  |
    Entonces el sistema debe mostrarle "Resumen de Termodinámica" y "Guía de Transferencia de Calor" como posibles similares

  Esquema del escenario: El sistema evalúa el umbral del 70% como punto de corte
    Cuando Ana solicita verificar similitud para un recurso cuyo contenido tiene un "<porcentaje>"% de similitud con "Resumen de Termodinámica"
    Entonces el sistema "<resultado>" mostrar el recurso "Resumen de Termodinámica" como similar

    Ejemplos:
      | porcentaje | resultado |
      | 69         | no debe   |
      | 70         | debe      |
      | 71         | debe      |

  # --- Decisión del usuario tras ver el recurso similar ---

  Escenario: El usuario decide continuar con la creación pese a la similitud detectada
    Dado que el sistema le mostró a Ana el recurso similar "Resumen de Termodinámica"
    Cuando Ana confirma que desea continuar con la creación de "Apuntes de Energía y Calor"
    Entonces el recurso "Apuntes de Energía y Calor" debe quedar creado
    Y Ana debe quedar registrada como propietaria del nuevo recurso

  Escenario: El usuario cancela la creación tras ver el recurso