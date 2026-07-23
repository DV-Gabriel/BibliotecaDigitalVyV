# language: es
Característica: Organizar recursos en colecciones personales
  Como usuario
  Quiero organizar en colecciones personales los recursos a los que tengo acceso
  Para personalizar mi espacio de aprendizaje sin alterar la propiedad, autoría ni el acceso de los recursos originales

  Antecedentes:
    Dado que existen los usuarios "Ana", "Luis" y "Marta"
    Y el usuario "Luis" está autenticado en el sistema
    Y el usuario tiene una colección personal llamada "Biología"

  Esquema del escenario: Agregar a una colección un recurso al que se tiene acceso
    Dado que existe un recurso "<visibilidad>" llamado "<recurso>"
    Y "<condicion_acceso>"
    Cuando el usuario agrega el recurso "<recurso>" a la colección "Biología"
    Entonces el recurso debe quedar incluido en la colección "Biología"

    Ejemplos:
      | visibilidad | recurso                        | condicion_acceso                                                |
      | público     | Introducción a la fotosíntesis | el recurso es de acceso público                                 |
      | privado     | Guía de laboratorio            | el propietario ha compartido "Guía de laboratorio" con "Luis"   |
      | privado     | Apuntes de química              | "Luis" es propietario del recurso                               |

  Escenario: No permitir agregar a una colección un recurso privado sin acceso específico (RN5)
    Dado que existe un recurso privado llamado "Material privado de física"
    Y el recurso no pertenece a "Luis" ni ha sido compartido con él
    Cuando el usuario intenta agregar el recurso "Material privado de física" a la colección "Biología"
    Entonces el sistema no debe permitir agregar el recurso a la colección

  Esquema del escenario: Mantener intactos la propiedad y la autoría del recurso al agregarlo a una colección
    Dado que existe un recurso público llamado "<recurso>"
    Y el "<atributo>" del recurso es "<valor>"
    Cuando el usuario agrega el recurso "<recurso>" a la colección "Biología"
    Entonces el "<atributo>" del recurso debe seguir siendo "<valor>"

    Ejemplos:
      | recurso                          | atributo    | valor         |
      | Historia de la educación         | propietario | Ana           |
      | Ensayo sobre literatura clásica  | autor       | Autor Externo |

  Escenario: No permitir modificar el recurso al organizarlo en una colección (RN6)
    Dado que existe un recurso público llamado "Lectura introductoria de filosofía"
    Y el propietario del recurso es "Ana"
    Cuando el usuario agrega el recurso "Lectura introductoria de filosofía" a la colección "Biología"
    Entonces "Luis" no debe convertirse en propietario del recurso
    Y "Luis" no debe poder modificar el recurso

  Esquema del escenario: El acceso a un recurso dentro de una colección se actualiza según el estado del recurso original
    Dado que existe un recurso privado llamado "<recurso>"
    Y el propietario compartió "<recurso>" con "Luis"
    Y el recurso "<recurso>" está incluido en la colección "Biología"
    Cuando "<evento>"
    Y el usuario consulta la colección "Biología"
    Entonces el usuario "<resultado>" acceder al recurso "<recurso>" desde la colección

    Ejemplos:
      | recurso                           | evento                                                                  | resultado     |
      | Material compartido de literatura | el propietario retira el acceso al recurso para "Luis"                 | no debe poder |
      | Material de astronomía            | el propietario marca el recurso "Material de astronomía" como público  | debe poder    |
