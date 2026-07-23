# language: es
Característica: Acceder a recursos compartidos por otros usuarios
  Como usuario
  Quiero ver y consultar los recursos que otros usuarios han compartido conmigo
  Para aprovechar el material que me ha sido otorgado

  Antecedentes:
    Dado que existen los usuarios "Ana", "Luis" y "Marta"
    Y el recurso "Ejercicios de Álgebra Lineal" es privado y pertenece a Luis
    Y el recurso "Apuntes de Química Orgánica" es privado y pertenece a Marta

  Escenario: Un usuario ve en su lista solo los recursos compartidos con él
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Ana consulta su lista de "recursos compartidos conmigo"
    Entonces debe ver el recurso "Ejercicios de Álgebra Lineal" en la lista
    Y no debe ver el recurso "Apuntes de Química Orgánica" en la lista

  Escenario: Un usuario puede abrir y consultar el contenido de un recurso compartido con él
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Ana abre el recurso "Ejercicios de Álgebra Lineal"
    Entonces debe poder visualizar su contenido completo

  Escenario: Un usuario no puede acceder a un recurso privado que no le ha sido compartido
    Cuando Ana intenta abrir el recurso "Apuntes de Química Orgánica"
    Entonces el sistema debe rechazar el acceso
    Y debe mostrar un mensaje indicando que no tiene permiso para ver ese recurso

  Escenario: Un usuario puede acceder a un recurso compartido con varios usuarios a la vez
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana y con Marta
    Cuando Marta abre el recurso "Ejercicios de Álgebra Lineal"
    Entonces debe poder visualizar su contenido completo

  Escenario: Cualquier usuario puede acceder a un recurso público sin necesidad de que se lo compartan
    Dado que existe el usuario "Carlos"
    Y el recurso "Introducción a la Física" es público y pertenece a Carlos
    Cuando Ana abre el recurso "Introducción a la Física"
    Entonces debe poder visualizar su contenido completo

  Escenario: Un usuario con acceso compartido no puede modificar el recurso
    Dado que "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Ana intenta editar el recurso "Ejercicios de Álgebra Lineal"
    Entonces el sistema debe rechazar la acción
    Y debe mostrar un mensaje indicando que solo el propietario puede modificar el recurso