# language: es

  Característica: Compartir y revocar acceso a recursos educativos digitales
  Como propietario de un recurso
  Quiero compartir mis recursos con otros usuarios y revocar ese acceso cuando lo decida
  Para controlar quién puede ver mi contenido

  Antecedentes: :
    Dado que existen los siguientes usuarios: "Ana", "Luis" y "Marta"
    Y el recurso "Ejercicios de Álgebra Lineal" es privado y pertenece a Luis

  # Compartir

  Escenario: El propietario comparte un recurso con otro usuario
    Cuando Luis comparte "Ejercicios de Álgebra Lineal" con Ana
    Entonces Ana debe tener acceso al recurso "Ejercicios de Álgebra Lineal"
    Y el recurso debe aparecer en la lista de "recursos compartidos conmigo" de Ana

  Escenario: El propietario comparte un recurso con varios usuarios
    Cuando Luis comparte "Ejercicios de Álgebra Lineal" con Ana y Marta
    Entonces Ana debe tener acceso al recurso "Ejercicios de Álgebra Lineal"
    Y Marta debe tener acceso al recurso "Ejercicios de Álgebra Lineal"

  Escenario: Un usuario que no es propietario no puede compartir el recurso
    Cuando Ana intenta compartir "Ejercicios de Álgebra Lineal" con Marta
    Entonces el sistema debe rechazar la acción
    Y debe mostrar un mensaje indicando que solo el propietario puede compartir el recurso

  Escenario: Un usuario con quien se compartió un recurso no puede volver a compartirlo con otros
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Ana intenta compartir "Ejercicios de Álgebra Lineal" con Marta
    Entonces el sistema debe rechazar la acción

  Escenario: Compartir un recurso que ya fue compartido con el mismo usuario
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Luis intenta compartir "Ejercicios de Álgebra Lineal" nuevamente con Ana
    Entonces el sistema no debe duplicar el acceso
    Y Ana debe seguir teniendo acceso al recurso

  # --- Revocar

  Escenario: El propietario revoca el acceso previamente otorgado
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Luis revoca el acceso de Ana a "Ejercicios de Álgebra Lineal"
    Entonces Ana ya no debe tener acceso al recurso "Ejercicios de Álgebra Lineal"
    Y el recurso no debe aparecer en la lista de "recursos compartidos conmigo" de Ana

  Escenario: Un usuario que no es propietario no puede revocar el acceso de otro
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana y con Marta
    Cuando Marta intenta revocar el acceso de Ana a "Ejercicios de Álgebra Lineal"
    Entonces el sistema debe rechazar la acción
    Y Ana debe seguir teniendo acceso al recurso

  Escenario: Revocar el acceso a un usuario que no tenía el recurso compartido
    Cuando Luis intenta revocar el acceso de Marta a "Ejercicios de Álgebra Lineal"
    Entonces el sistema no debe generar ningún cambio
    Y debe indicar que Marta no tenía acceso al recurso

