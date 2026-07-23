# language: es

Característica: Guardar y publicar recursos como borrador
  Como usuario
  Quiero poder guardar el progreso de un recurso incompleto y retomarlo después
  Para no perder mi trabajo mientras completo los datos obligatorios antes de publicarlo (RN1, RN12)

  Antecedentes:
    Dado que "Ana" es un usuario autenticado en el sistema

  Escenario: Guardar un recurso incompleto como borrador
    Cuando Ana empieza a crear un recurso con título "Guía de Estadística" y sale sin completar la categoría ni las etiquetas
    Entonces el recurso "Guía de Estadística" debe quedar guardado con estado "borrador"
    Y el recurso no debe aparecer en el catálogo público

  Escenario: Reanudar la edición de un borrador propio
    Dado que el recurso "Guía de Estadística" quedó guardado como borrador con el contenido que Ana había ingresado
    Cuando Ana retoma la edición de "Guía de Estadística"
    Entonces debe ver el contenido que había guardado previamente

  Escenario: Un borrador solo es visible para su propietario
    Dado que Ana tiene el recurso "Guía de Estadística" guardado como "borrador"
    Cuando Luis intenta consultar el recurso "Guía de Estadística"
    Entonces el sistema debe rechazar el acceso

  Escenario: No permitir compartir un recurso en borrador
    Dado que Ana tiene el recurso "Guía de Estadística" guardado como "borrador"
    Cuando Ana intenta compartir "Guía de Estadística" con Luis
    Entonces el sistema debe rechazar la acción
    Y debe indicar que el recurso debe completarse y publicarse antes de compartirse

  Escenario: Publicar un borrador al completar los campos obligatorios
    Dado que Ana tiene el recurso "Guía de Estadística" guardado como "borrador"
    Y Ana completa título, descripción, categoría y al menos una etiqueta
    Cuando Ana publica el recurso "Guía de Estadística"
    Entonces el recurso debe quedar con estado "publicado"
    Y el recurso debe quedar visible según su visibilidad configurada

  Esquema del escenario: No permitir publicar mientras falte un campo obligatorio
    Dado que Ana tiene el recurso "Guía de Estadística" guardado como "borrador" sin "<campo>"
    Cuando Ana intenta publicar "Guía de Estadística"
    Entonces el sistema debe impedir la publicación
    Y debe indicar que "<mensaje>"

    Ejemplos:
      | campo       | mensaje                                     |
      | título      | el título es obligatorio                    |
      | descripción | la descripción es obligatoria               |
      | categoría   | la categoría es obligatoria                 |
      | etiquetas   | el recurso debe tener al menos una etiqueta |