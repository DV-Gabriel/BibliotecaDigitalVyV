# Created by Javier at 9/7/2026
# language: es

Característica: Organizar recursos en colecciones
  Como estudiante o docente
  Quiero organizar recursos educativos accesibles en colecciones personales
  Para personalizar mi espacio de aprendizaje y encontrar fácilmente los materiales que necesito

  Antecedentes:
    Dado que el usuario "Estudiante Luis" está autenticado en el sistema

  Escenario: Crear una colección personal para organizar recursos educativos
    Cuando el usuario crea una colección personal llamada "Biología"
    Entonces la colección "Biología" debe quedar disponible en su espacio personal de aprendizaje

  Escenario: Agregar un recurso público a una colección personal
    Dado que existe un recurso público llamado "Introducción a la fotosíntesis"
    Y el usuario tiene una colección personal llamada "Biología"
    Cuando el usuario agrega el recurso "Introducción a la fotosíntesis" a la colección "Biología"
    Entonces el recurso debe quedar incluido en la colección "Biología"
    Y el usuario debe poder ver el recurso dentro de esa colección

  Escenario: Agregar a una colección personal un recurso compartido específicamente con el usuario
    Dado que existe un recurso privado llamado "Guía de laboratorio"
    Y el propietario del recurso ha compartido "Guía de laboratorio" con "Estudiante Luis"
    Y el usuario tiene una colección personal llamada "Laboratorio"
    Cuando el usuario agrega el recurso "Guía de laboratorio" a la colección "Laboratorio"
    Entonces el recurso debe quedar incluido en la colección "Laboratorio"
    Y el usuario debe poder ver el recurso dentro de esa colección

  Escenario: Agregar un recurso propio privado a una colección personal
    Dado que "Estudiante Luis" es propietario de un recurso privado llamado "Apuntes de química"
    Y el usuario tiene una colección personal llamada "Química"
    Cuando el usuario agrega el recurso "Apuntes de química" a la colección "Química"
    Entonces el recurso debe quedar incluido en la colección "Química"
    Y el recurso debe seguir siendo privado

  Escenario: No permitir agregar a una colección un recurso privado sin acceso específico
    Dado que existe un recurso privado llamado "Material privado de física"
    Y el recurso no pertenece a "Estudiante Luis"
    Y el recurso no ha sido compartido con "Estudiante Luis"
    Y el usuario tiene una colección personal llamada "Física"
    Cuando el usuario intenta agregar el recurso "Material privado de física" a la colección "Física"
    Entonces el sistema no debe permitir agregar el recurso a la colección
    Y el recurso no debe aparecer en la colección "Física"

  Escenario: Mantener la propiedad del recurso al agregarlo a una colección
    Dado que existe un recurso público llamado "Historia de la educación"
    Y el propietario del recurso es "Docente Ana"
    Y el usuario tiene una colección personal llamada "Historia"
    Cuando el usuario agrega el recurso "Historia de la educación" a la colección "Historia"
    Entonces el recurso debe quedar incluido en la colección "Historia"
    Y el propietario del recurso debe seguir siendo "Docente Ana"

  Escenario: Mantener el autor del recurso al agregarlo a una colección
    Dado que existe un recurso público llamado "Ensayo sobre literatura clásica"
    Y el autor del recurso es "Autor Externo"
    Y el usuario tiene una colección personal llamada "Literatura"
    Cuando el usuario agrega el recurso "Ensayo sobre literatura clásica" a la colección "Literatura"
    Entonces el recurso debe quedar incluido en la colección "Literatura"
    Y el autor del recurso debe seguir siendo "Autor Externo"

  Escenario: Mantener la visibilidad original del recurso al agregarlo a una colección
    Dado que existe un recurso privado llamado "Plan de estudio personalizado"
    Y el propietario del recurso ha compartido "Plan de estudio personalizado" con "Estudiante Luis"
    Y el usuario tiene una colección personal llamada "Planificación"
    Cuando el usuario agrega el recurso "Plan de estudio personalizado" a la colección "Planificación"
    Entonces el recurso debe quedar incluido en la colección "Planificación"
    Y el recurso debe seguir siendo privado
    Y solo los usuarios con acceso permitido deben poder visualizarlo

  Escenario: Organizar un mismo recurso accesible en más de una colección personal
    Dado que existe un recurso público llamado "Mapa conceptual de ecología"
    Y el usuario tiene una colección personal llamada "Biología"
    Y el usuario tiene una colección personal llamada "Medio ambiente"
    Cuando el usuario agrega el recurso "Mapa conceptual de ecología" a la colección "Biología"
    Y agrega el recurso "Mapa conceptual de ecología" a la colección "Medio ambiente"
    Entonces el recurso debe quedar incluido en la colección "Biología"
    Y el recurso debe quedar incluido en la colección "Medio ambiente"

  Escenario: Evitar duplicar el mismo recurso dentro de una misma colección personal
    Dado que existe un recurso público llamado "Resumen de anatomía"
    Y el usuario tiene una colección personal llamada "Medicina"
    Y el recurso "Resumen de anatomía" ya está incluido en la colección "Medicina"
    Cuando el usuario intenta agregar nuevamente el recurso "Resumen de anatomía" a la colección "Medicina"
    Entonces la colección "Medicina" debe contener una sola vez el recurso "Resumen de anatomía"

  Escenario: Quitar un recurso de una colección personal sin eliminar el recurso del sistema
    Dado que existe un recurso público llamado "Línea de tiempo histórica"
    Y el usuario tiene una colección personal llamada "Historia"
    Y el recurso "Línea de tiempo histórica" está incluido en la colección "Historia"
    Cuando el usuario quita el recurso "Línea de tiempo histórica" de la colección "Historia"
    Entonces el recurso no debe aparecer en la colección "Historia"
    Y el recurso debe seguir existiendo en el sistema

  Escenario: Quitar un recurso de una colección sin modificar sus datos
    Dado que existe un recurso público llamado "Conceptos básicos de geometría"
    Y el recurso tiene la categoría "Matemáticas"
    Y el recurso tiene la etiqueta "geometría"
    Y el usuario tiene una colección personal llamada "Matemáticas"
    Y el recurso "Conceptos básicos de geometría" está incluido en la colección "Matemáticas"
    Cuando el usuario quita el recurso "Conceptos básicos de geometría" de la colección "Matemáticas"
    Entonces el recurso no debe aparecer en la colección "Matemáticas"
    Y la categoría del recurso debe seguir siendo "Matemáticas"
    Y el recurso debe conservar la etiqueta "geometría"

  Escenario: Ver los recursos organizados dentro de una colección personal
    Dado que el usuario tiene una colección personal llamada "Ciencias"
    Y la colección "Ciencias" contiene el recurso público "Introducción a la biología"
    Y la colección "Ciencias" contiene el recurso público "Conceptos básicos de química"
    Cuando el usuario consulta la colección "Ciencias"
    Entonces debe ver el recurso "Introducción a la biología"
    Y debe ver el recurso "Conceptos básicos de química"

  Escenario: No mostrar en una colección un recurso privado cuyo acceso fue retirado al usuario
    Dado que existe un recurso privado llamado "Material compartido de literatura"
    Y el propietario del recurso compartió "Material compartido de literatura" con "Estudiante Luis"
    Y el usuario tiene una colección personal llamada "Literatura"
    Y el recurso "Material compartido de literatura" está incluido en la colección "Literatura"
    Cuando el propietario retira el acceso al recurso para "Estudiante Luis"
    Y el usuario consulta la colección "Literatura"
    Entonces el usuario no debe poder acceder al recurso "Material compartido de literatura" desde la colección "Literatura"

  Escenario: Conservar en una colección el acceso a un recurso que pasa a ser público
    Dado que existe un recurso privado llamado "Material de astronomía"
    Y el propietario del recurso compartió "Material de astronomía" con "Estudiante Luis"
    Y el usuario tiene una colección personal llamada "Astronomía"
    Y el recurso "Material de astronomía" está incluido en la colección "Astronomía"
    Cuando el propietario marca el recurso "Material de astronomía" como público
    Y el usuario consulta la colección "Astronomía"
    Entonces el usuario debe poder acceder al recurso "Material de astronomía" desde la colección "Astronomía"

  Escenario: No permitir modificar el recurso al organizarlo en una colección
    Dado que existe un recurso público llamado "Lectura introductoria de filosofía"
    Y el propietario del recurso es "Docente Ana"
    Y el usuario tiene una colección personal llamada "Filosofía"
    Cuando el usuario agrega el recurso "Lectura introductoria de filosofía" a la colección "Filosofía"
    Entonces el recurso debe quedar incluido en la colección "Filosofía"
    Y "Estudiante Luis" no debe convertirse en propietario del recurso
    Y "Estudiante Luis" no debe poder modificar el recurso