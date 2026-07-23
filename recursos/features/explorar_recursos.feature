# language: es
Característica: Explorar y buscar recursos digitales en el catálogo
  Como usuario
  Quiero que el catálogo me muestre únicamente los recursos a los que tengo acceso (RN5)
  Para encontrar material de mi interés sin exponer contenido privado de otros usuarios

  Antecedentes:
    Dado que existen los siguientes recursos en el sistema:
      | titulo                       | visibilidad | propietario |
      | Introducción a la Física     | publico     | Carlos      |
      | Cálculo Diferencial          | publico     | Ana         |
      | Apuntes de Química Orgánica  | privado     | Marta       |
      | Ejercicios de Álgebra Lineal | compartido  | Luis        |

  Escenario: Un recurso privado no aparece en la búsqueda de otro usuario
    Cuando Ana busca "Química Orgánica" en el catálogo
    Entonces no debe ver el recurso "Apuntes de Química Orgánica" en los resultados

  Escenario: Un recurso público sí aparece para cualquier usuario
    Cuando Ana busca "Física" en el catálogo
    Entonces debe ver el recurso "Introducción a la Física" en los resultados

  Escenario: Un recurso compartido aparece solo para el usuario con quien fue compartido
    Dado que el recurso "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Ana busca "Álgebra Lineal" en el catálogo
    Entonces debe ver el recurso "Ejercicios de Álgebra Lineal" en los resultados

  Escenario: Un recurso compartido no aparece para un usuario ajeno al que se compartió
    Dado que el recurso "Ejercicios de Álgebra Lineal" fue compartido por Luis con Ana
    Cuando Marta busca "Álgebra Lineal" en el catálogo
    Entonces no debe ver el recurso "Ejercicios de Álgebra Lineal" en los resultados

  Esquema del escenario: Mostrar el rol del autor como indicador de confianza
    Dado que el recurso "<recurso>" tiene como autor a un usuario con rol "<rol>"
    Cuando Ana consulta el recurso "<recurso>"
    Entonces debe ver que el autor tiene el rol "<rol>"

    Ejemplos:
      | recurso                    | rol         |
      | Introducción a la Física   | docente     |
      | Apuntes de clase de Luis   | estudiante  |

  Escenario: No mostrar rol cuando el autor es externo
    Dado que el recurso "Principios de Economía" tiene como autor externo a "Adam Smith"
    Cuando Ana consulta el recurso "Principios de Economía"
    Entonces el sistema no debe mostrar ningún rol asociado al autor
