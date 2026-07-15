# language: es

Característica: : Editar mis propios recursos educativos digitales (Actualizar recursos propios)
  Como estudiante o docente
  Quiero modificar la información de los recursos que he creado
  Para mantener el contenido actualizado y corregir posibles errores

  Antecedentes: :
    Dado que existen los siguientes usuarios: "Ana", "Luis" y "Marta"
    Y el usuario "Luis" está autenticado en el sistema
    Y "Luis" ha creado el recurso "Apuntes de Álgebra" con:
      | campo       | valor                 |
      | descripción | Resumen de vectores   |
      | categoría   | Matemáticas           |
      | etiquetas   | vectores, álgebra     |
      | autor       | Luis                  |

  # --- Edición Exitosa ---

  Escenario: Editar el título y la descripción de un recurso propio
    Cuando el usuario modifica el título del recurso a "Apuntes de Álgebra Lineal"
    Y modifica la descripción a "Resumen detallado de vectores y matrices"
    Entonces el recurso debe actualizarse con el nuevo título y descripción
    Y Luis debe seguir siendo el propietario del recurso

  Escenario: Cambiar la categoría de un recurso propio
    Cuando el usuario cambia la categoría del recurso a "Ciencias Exactas"
    Entonces el recurso debe mostrar la nueva categoría "Ciencias Exactas"

  Escenario: Actualizar etiquetas de un recurso propio
    Cuando el usuario agrega la etiqueta "matrices" al recurso
    Y quita la etiqueta "vectores"
    Entonces el recurso debe tener las etiquetas "álgebra" y "matrices"

  Escenario: Cambiar el autor (externo) de un recurso propio
    Cuando el usuario modifica el autor del recurso a "Autor Externo de Referencia"
    Entonces el recurso debe mostrar el nuevo autor "Autor Externo de Referencia"

  # --- Restricciones de Propiedad (Regla 6) ---

  Escenario: Un usuario no puede editar un recurso que no ha creado
    Dado que "Ana" ha creado el recurso "Guía de Biología"
    Cuando Luis intenta editar el recurso "Guía de Biología"
    Entonces el sistema debe rechazar la acción
    Y debe mostrar un mensaje indicando que solo el propietario puede modificar el recurso

  # --- Validaciones de Reglas de Negocio (Regla 1 y 7) ---

  Escenario: No permitir dejar el título vacío al editar
    Cuando el usuario intenta borrar el título del recurso "Apuntes de Álgebra"
    Entonces el sistema debe impedir guardar los cambios
    Y debe indicar que el título es obligatorio

  Escenario: No permitir dejar la descripción vacía al editar
    Cuando el usuario intenta borrar la descripción del recurso "Apuntes de Álgebra"
    Entonces el sistema debe impedir guardar los cambios
    Y debe indicar que la descripción es obligatoria

  Escenario: No permitir dejar el recurso sin etiquetas al editar
    Cuando el usuario intenta quitar todas las etiquetas del recurso "Apuntes de Álgebra"
    Entonces el sistema debe impedir guardar los cambios
    Y debe indicar que el recurso debe tener al menos una etiqueta

  Escenario: No permitir dejar el recurso sin categoría al editar
    Cuando el usuario intenta desvincular la categoría del recurso "Apuntes de Álgebra"
    Entonces el sistema debe impedir guardar los cambios
    Y debe indicar que la categoría es obligatoria