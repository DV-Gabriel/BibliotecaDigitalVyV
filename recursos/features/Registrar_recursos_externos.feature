# language: en
Feature: Registrar recursos educativos de autores externos
  Como usuario
  Quiero registrar en el sistema recursos cuyo autor original no es un usuario registrado
  Para preservar y compartir material de valor educativo que no fue creado en la plataforma

  Background:
    Given that the users "Ana", "Luis" and "Marta" exist
    And the user "Ana" is authenticated in the system

  Scenario: Registrar un recurso completo con autor externo
    When Ana registers a resource with:
      | campo       | valor                         |
      | título      | Principios de Economía        |
      | descripción | Fundamentos de microeconomía  |
      | categoría   | Economía                      |
      | etiquetas   | economia, microeconomia       |
      | autor       | Adam Smith                    |
      | visibilidad | público                       |
    Then the resource "Principios de Economía" should be registered in the system
    And "Adam Smith" should be set as the resource author
    And "Ana" should be set as the owner of the resource

  Scenario: El autor externo no se convierte en usuario ni en propietario del sistema
    Given that Ana registers the resource "Principios de Economía" with external author "Adam Smith"
    Then "Adam Smith" should not appear as a system user
    And "Adam Smith" should not have owner permissions over the resource

  Scenario Outline: No permitir registrar un recurso sin los datos obligatorios
    When Ana attempts to register a resource "<situacion>"
    Then the system should prevent registering the resource
    And it should indicate "<mensaje>"

    Examples:
      | situacion                     | mensaje                                     |
      | sin título                    | el título es obligatorio                    |
      | sin descripción               | la descripción es obligatoria               |
      | sin categoría asociada        | la categoría es obligatoria                 |
      | sin ninguna etiqueta          | el recurso debe tener al menos una etiqueta |

  Scenario: Registrar un recurso sin especificar autor externo asume como autor al propietario
    When Ana registers a resource with:
      | campo       | valor                      |
      | título      | Notas de clase de Cálculo  |
      | descripción | Apuntes propios de clase   |
      | categoría   | Matemáticas                |
      | etiquetas   | calculo                    |
      | visibilidad | privado                    |
    Then the resource "Notas de clase de Cálculo" should be registered with author "Ana"
    And "Ana" should be set as the owner of the resource

  Scenario: Registrar un recurso como privado y compartirlo posteriormente
    Given that Ana registers the resource "Guía de Historia Antigua" with external author "Heródoto" and private visibility
    When Ana shares "Guía de Historia Antigua" with Luis
    Then Luis should have access to the resource "Guía de Historia Antigua"
    And the author of the resource should remain "Heródoto"