# language: en

Feature: Guardar y publicar recursos como borrador
  Como usuario
  Quiero poder guardar el progreso de un recurso incompleto y retomarlo después
  Para no perder mi trabajo mientras completo los datos obligatorios antes de publicarlo (RN1, RN12)

  Background:
    Given that "Ana" is an authenticated user in the system

  Scenario: Guardar un recurso incompleto como borrador
    When Ana begins creating a resource titled "Guía de Estadística" and exits without completing category or tags
    Then the resource "Guía de Estadística" should be saved with state "borrador"
    And the resource should not appear in the public catalog

  Scenario: Reanudar la edición de un borrador propio
    Given that the resource "Guía de Estadística" was saved as a draft with the content Ana entered
    When Ana resumes editing "Guía de Estadística"
    Then she should see the content she had previously saved

  Scenario: Un borrador solo es visible para su propietario
    Given that Ana has the resource "Guía de Estadística" saved as a "borrador"
    When Luis attempts to view the resource "Guía de Estadística"
    Then the system should deny access

  Scenario: No permitir compartir un recurso en borrador
    Given that Ana has the resource "Guía de Estadística" saved as a "borrador"
    When Ana attempts to share "Guía de Estadística" with Luis
    Then the system should reject the action
    And it should indicate that the resource must be completed and published before sharing

  Scenario: Publicar un borrador al completar los campos obligatorios
    Given that Ana has the resource "Guía de Estadística" saved as a "borrador"
    And Ana completes title, description, category and at least one tag
    When Ana publishes the resource "Guía de Estadística"
    Then the resource should have state "publicado"
    And the resource should be visible according to its configured visibility

  Scenario Outline: No permitir publicar mientras falte un campo obligatorio
    Given that Ana has the resource "Guía de Estadística" saved as a "borrador" without "<campo>"
    When Ana attempts to publish "Guía de Estadística"
    Then the system should prevent publication
    And it should indicate "<mensaje>"

    Examples:
      | campo       | mensaje                                     |
      | título      | el título es obligatorio                    |
      | descripción | la descripción es obligatoria               |
      | categoría   | la categoría es obligatoria                 |
      | etiquetas   | el recurso debe tener al menos una etiqueta |