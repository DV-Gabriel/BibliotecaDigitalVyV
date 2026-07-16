# language: es

  #Se retiró: coincidencia exacta/parcial de título, búsqueda por palabra clave en descripción,
  # mensaje de "no se encontraron resultados", filtrar por categoría sin resultados, y el Esquema
  # del escenario que combina texto + categoría. Todo esto es mecánica de motor de búsqueda (cómo
  #  hace matching el sistema), sin ninguna Regla de Negocio que lo respalde.
  #
  #Se conserva únicamente lo que prueba RN5 (visibilidad/control de acceso), que es la única regla
  # de negocio que aplica a este feature.

  #Cuando reduje el feature 7 a solo los escenarios que prueban RN5 (visibilidad/acceso), eliminé los
  # escenarios que usaban descripcion y categoria como criterio de búsqueda/filtro (buscar por palabra
  # clave en la descripción, filtrar por categoría). Como esos escenarios ya no están en el feature,
  # ninguna fila Cuando/Entonces restante lee o verifica esas columnas — quedarían en la tabla de
  # Antecedentes sin que ningún escenario las use, que es justo el tipo de "ruido" que se recomienda
  # evitar en un Background: datos que el lector tiene que procesar sin que aporten a ninguna aserción posterior.
  #Por qué esto NO contradice RN1/RN7
  #Tienes razón en que categoría y etiqueta son obligatorias por RN1 y RN7 — pero esa regla dice que
  # un recurso no puede crearse/publicarse sin ellas, no que la búsqueda deba filtrar por ellas. Esa
  # regla ya está correctamente probada en:
  #
  #Feature 6 (Editar): "No permitir dejar el recurso sin categoría/etiqueta al editar"
  #Feature 9 (Registrar): "No permitir registrar un recurso sin categoría/sin etiquetas"
  #
  #En el feature 7, los recursos del Antecedentes ya existen como precondición (asumimos que
  # fueron creados correctamente, con categoría y etiqueta, porque RN1/RN7 así lo exigen en otro
  # lado). El feature 7 no vuelve a probar que existan — solo prueba que la visibilidad determina
  # quién los ve. Repetir esa validación aquí sería duplicar cobertura de una regla que ya está probada
  # en otro feature, sin agregar valor.

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