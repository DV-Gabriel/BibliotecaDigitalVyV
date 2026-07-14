# Created by Javier at 9/7/2026
# language: es

Característica: Crear recursos educativos originales
  Como usuario del sistema
  Quiero crear recursos educativos originales completando la información obligatoria
  Para publicar materiales educativos correctamente identificados y disponibles según su visibilidad

  Antecedentes:
    Dado que el usuario "Docente Ana" está autenticado en el sistema

  Escenario: Crear y publicar un recurso educativo original con todos los datos obligatorios
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Introducción a la fotosíntesis               |
      | descripción | Material introductorio sobre la fotosíntesis |
      | categoría   | Ciencias                                     |
      | etiquetas   | biología, plantas                            |
      | autor       | Docente Ana                                  |
    Y publica el recurso
    Entonces el recurso debe quedar publicado correctamente
    Y el propietario del recurso debe ser "Docente Ana"
    Y el autor del recurso debe ser "Docente Ana"
    Y el recurso debe quedar privado por defecto
    Y solo el propietario debe poder visualizarlo mientras no sea público ni compartido

  Escenario: No permitir publicar un recurso original sin título
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | descripción | Material introductorio sobre la fotosíntesis |
      | categoría   | Ciencias                                     |
      | etiquetas   | biología, plantas                            |
      | autor       | Docente Ana                                  |
    Y intenta publicar el recurso
    Entonces el sistema no debe permitir la publicación
    Y debe informar que el título es obligatorio

  Escenario: No permitir publicar un recurso original sin descripción
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título    | Introducción a la fotosíntesis |
      | categoría | Ciencias                       |
      | etiquetas | biología, plantas              |
      | autor     | Docente Ana                    |
    Y intenta publicar el recurso
    Entonces el sistema no debe permitir la publicación
    Y debe informar que la descripción es obligatoria

  Escenario: No permitir publicar un recurso original sin categoría
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Introducción a la fotosíntesis               |
      | descripción | Material introductorio sobre la fotosíntesis |
      | etiquetas   | biología, plantas                            |
      | autor       | Docente Ana                                  |
    Y intenta publicar el recurso
    Entonces el sistema no debe permitir la publicación
    Y debe informar que la categoría es obligatoria

  Escenario: No permitir publicar un recurso original sin etiquetas
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Introducción a la fotosíntesis               |
      | descripción | Material introductorio sobre la fotosíntesis |
      | categoría   | Ciencias                                     |
      | autor       | Docente Ana                                  |
    Y intenta publicar el recurso
    Entonces el sistema no debe permitir la publicación
    Y debe informar que al menos una etiqueta es obligatoria

  Escenario: No permitir publicar un recurso original sin autor identificado
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Introducción a la fotosíntesis               |
      | descripción | Material introductorio sobre la fotosíntesis |
      | categoría   | Ciencias                                     |
      | etiquetas   | biología, plantas                            |
    Y intenta publicar el recurso
    Entonces el sistema no debe permitir la publicación
    Y debe informar que el autor es obligatorio

  Escenario: Asignar como propietario al usuario que crea el recurso original
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Guía básica de álgebra         |
      | descripción | Recurso original sobre álgebra |
      | categoría   | Matemáticas                    |
      | etiquetas   | álgebra                        |
      | autor       | Docente Ana                    |
    Y publica el recurso
    Entonces el propietario del recurso debe ser "Docente Ana"
    Y el propietario debe poder modificar el recurso

  Escenario: Mantener privado por defecto un recurso original recién publicado
    Cuando el usuario crea un recurso educativo original con los siguientes datos:
      | título      | Guía básica de álgebra         |
      | descripción | Recurso original sobre álgebra |
      | categoría   | Matemáticas                    |
      | etiquetas   | álgebra                        |
      | autor       | Docente Ana                    |
    Y publica el recurso
    Entonces el recurso debe quedar privado por defecto
    Y el recurso no debe estar disponible para otros usuarios que no tengan acceso específico

  Escenario: Permitir que el propietario publique un recurso original como público
    Dado que el usuario ha creado y publicado un recurso educativo original privado
    Cuando el propietario marca el recurso como público
    Entonces el recurso debe quedar visible para otros usuarios del sistema

  Escenario: No permitir que otro usuario modifique un recurso original que no le pertenece
    Dado que "Docente Ana" ha publicado un recurso educativo original
    Y el usuario "Estudiante Luis" está autenticado en el sistema
    Cuando "Estudiante Luis" intenta modificar el recurso de "Docente Ana"
    Entonces el sistema no debe permitir la modificación
    Y debe mantener sin cambios la información del recurso

  Escenario: Permitir que el propietario edite los datos de su recurso original publicado
    Dado que el usuario ha creado y publicado un recurso educativo original con los siguientes datos:
      | título      | Guía básica de álgebra         |
      | descripción | Recurso original sobre álgebra |
      | categoría   | Matemáticas                    |
      | etiquetas   | álgebra                        |
      | autor       | Docente Ana                    |
    Cuando el propietario actualiza la descripción del recurso a "Recurso actualizado sobre conceptos básicos de álgebra"
    Entonces el sistema debe guardar la nueva descripción
    Y el recurso debe conservar a "Docente Ana" como propietario

  Escenario: No permitir dejar incompleto un recurso original publicado al editarlo
    Dado que el usuario ha creado y publicado un recurso educativo original con los siguientes datos:
      | título      | Guía básica de álgebra         |
      | descripción | Recurso original sobre álgebra |
      | categoría   | Matemáticas                    |
      | etiquetas   | álgebra                        |
      | autor       | Docente Ana                    |
    Cuando el propietario elimina todas las etiquetas del recurso
    Y intenta guardar los cambios
    Entonces el sistema no debe permitir guardar la modificación
    Y debe informar que al menos una etiqueta es obligatoria
