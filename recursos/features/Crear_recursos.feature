# language: en

Feature: Crear recursos personalizados originales (detección de similitud por contenido)
  Como usuario
  Quiero que el sistema me advierta si el contenido de mi recurso es significativamente similar a uno existente (RN9)
  Para reutilizar información existente o reestructurar mi recurso y aportar algo distinto

  Background:
    Given that "Ana" is an authenticated user in the system
    And the resource "Resumen de Termodinámica", created by "Luis", exists with the following paragraph:
      """
      La termodinámica estudia las relaciones entre el calor, el trabajo y la energía
      en los sistemas físicos, así como sus transformaciones.
      """

  Scenario Outline: El sistema advierte al usuario según el nivel de similitud del contenido (RN9)
    When Ana requests similarity check for a resource with content "<nivel_similitud>" to "Resumen de Termodinámica"
    Then the system "<resultado>" warn Ana about the resource "Resumen de Termodinámica" as a possible similar

    Examples:
      | nivel_similitud       | resultado    |
      | claramente distinto   | no debe      |
      | significativamente similar | debe    |

  Scenario: El sistema detecta varios recursos significativamente similares y los muestra todos (RN9)
    Given that another resource "Guía de Transferencia de Calor", created by "Marta", exists with content significantly similar to "Resumen de Termodinámica"
    When Ana requests similarity check for the resource "Apuntes de Energía y Calor"
    Then the system should warn her about "Resumen de Termodinámica" and "Guía de Transferencia de Calor" as possible similars

  # --- Decisión del usuario tras ver el recurso similar ---

  Scenario: El usuario decide continuar con la creación pese a la similitud detectada
    Given that the system warned Ana about the similar resource "Resumen de Termodinámica"
    When Ana confirms she wants to continue creating "Apuntes de Energía y Calor"
    Then the resource "Apuntes de Energía y Calor" should be created
    And Ana should be recorded as the owner of the new resource

  Scenario: El usuario cancela la creación tras ver el recurso similar
    Given that the system warned Ana about the similar resource "Resumen de Termodinámica"
    When Ana cancels the creation of "Apuntes de Energía y Calor"
    Then the resource "Apuntes de Energía y Calor" should not be created
    And the resource "Resumen de Termodinámica" should remain unchanged
