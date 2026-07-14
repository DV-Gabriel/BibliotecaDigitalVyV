# language: es

Característica: Explorar y buscar recursos digitales en el catálogo

  Como usuario
  Quiero buscar y filtrar recursos educativos en el catálogo
  Para encontrar rápidamente el material de mi interes

  Antecedentes:
    Dado que existen los siguientes recursos en el sistema:
      | titulo                       | descripcion                           | categoria   | etiquetas        | visibilidad | propietario |
      | Introducción a la Física     | Conceptos básicos de mecánica clásica | Física      | mecanica, fisica | publico     | Carlos      |
      | Cálculo Diferencial          | Guía de derivadas e integrales        | Matemáticas | calculo, algebra | publico     | Ana         |
      | Apuntes de Química Orgánica  | Reacciones y compuestos orgánicos     | Química     | organica         | privado     | Marta       |
      | Ejercicios de Álgebra Lineal | Matrices y sistemas de ecuaciones     | Matemáticas | algebra          | compartido  | Luis        |


    # Búsqueda por título

  Escenario: Buscar un recurso por coincidencia exacta de título
    Cuando Ana busca "Cálculo Diferencial" en el catálogo
    Entonces debe ver el recurso "Cálculo Diferencial" en los resultados

  Escenario: Buscar un recurso por coincidencia parcial de título
    Cuando Ana busca "Física" en el catálogo
    Entonces debe ver el recurso "Introducción a la Física" en los resultados

  Escenario: Buscar un título que no existe en el catálogo
    Cuando Ana busca "Historia del Arte" en el catálogo
    Entonces no debe ver ningún resultado
    Y debe ver un mensaje indicando que no se encontraron recursos

  # Búsqueda por descripción

  Escenario: Buscar un recurso por palabra clave en la descripción
    Cuando Ana busca "derivadas" en el catálogo
    Entonces debe ver el recurso "Cálculo Diferencial" en los resultados

  # Filtro por categoría

  Escenario: Filtrar recursos por categoría
    Cuando Ana filtra el catálogo por la categoría "Matemáticas"
    Entonces debe ver el recurso "Cálculo Diferencial" en los resultados
    Y debe ver el recurso "Ejercicios de Álgebra Lineal" en los resultados
    Y no debe ver el recurso "Introducción a la Física" en los resultados

  Escenario: Filtrar por una categoría sin recursos asociados
    Cuando Ana filtra el catálogo por la categoría "Historia"
    Entonces no debe ver ningún resultado

  # --- Combinación de búsqueda y filtro ---

  Esquema del escenario: Buscar texto dentro de una categoría específica
    Cuando Ana busca "<texto>" filtrando por la categoría "<categoria>"
    Entonces debe ver el recurso "<resultado_esperado>" en los resultados

    Ejemplos:
      | texto    | categoria   | resultado_esperado           |
      | algebra  | Matemáticas | Cálculo Diferencial          |
      | matrices | Matemáticas | Ejercicios de Álgebra Lineal |

  # Regla de negocio 5: visibilidad

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
