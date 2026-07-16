# language: es
Característica: Registrar recursos educativos de autores externos
  Como usuario
  Quiero registrar en el sistema recursos cuyo autor original no es un usuario registrado
  Para preservar y compartir material de valor educativo que no fue creado en la plataforma

  Antecedentes:
    Dado que existen los usuarios "Ana", "Luis" y "Marta"
    Y el usuario "Ana" está autenticado en el sistema

  Escenario: Registrar un recurso completo con autor externo
    Cuando Ana registra un recurso con:
      | campo       | valor                         |
      | título      | Principios de Economía        |
      | descripción | Fundamentos de microeconomía  |
      | categoría   | Economía                      |
      | etiquetas   | economia, microeconomia       |
      | autor       | Adam Smith                    |
      | visibilidad | público                       |
    Entonces el recurso "Principios de Economía" debe quedar registrado en el sistema
    Y "Adam Smith" debe quedar como autor del recurso
    Y "Ana" debe quedar como propietaria del recurso

  Escenario: El autor externo no se convierte en usuario ni en propietario del sistema
    Dado que Ana registra el recurso "Principios de Economía" con autor externo "Adam Smith"
    Entonces "Adam Smith" no debe aparecer como usuario del sistema
    Y "Adam Smith" no debe tener permisos de propietario sobre el recurso

  Esquema del escenario: No permitir registrar un recurso sin los datos obligatorios
    Cuando Ana intenta registrar un recurso "<situacion>"
    Entonces el sistema debe impedir el registro del recurso
    Y debe indicar que "<mensaje>"

    Ejemplos:
      | situacion                     | mensaje                                     |
      | sin título                    | el título es obligatorio                    |
      | sin descripción               | la descripción es obligatoria               |
      | sin categoría asociada        | la categoría es obligatoria                 |
      | sin ninguna etiqueta          | el recurso debe tener al menos una etiqueta |

  Escenario: Registrar un recurso sin especificar autor externo asume como autor al propietario
    Cuando Ana registra un recurso con:
      | campo       | valor                      |
      | título      | Notas de clase de Cálculo  |
      | descripción | Apuntes propios de clase   |
      | categoría   | Matemáticas                |
      | etiquetas   | calculo                    |
      | visibilidad | privado                    |
    Entonces el recurso "Notas de clase de Cálculo" debe quedar registrado con autor "Ana"
    Y "Ana" debe quedar como propietaria del recurso

  Escenario: Registrar un recurso como privado y compartirlo posteriormente
    Dado que Ana registra el recurso "Guía de Historia Antigua" con autor externo "Heródoto" y visibilidad privada
    Cuando Ana comparte "Guía de Historia Antigua" con Luis
    Entonces Luis debe tener acceso al recurso "Guía de Historia Antigua"
    Y el autor del recurso debe seguir siendo "Heródoto"