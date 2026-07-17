# language: en
Feature: Gestionar favoritos y marcadores de acceso rápido
  Como usuario
  Quiero que mis favoritos respeten en todo momento el acceso vigente al recurso original (RN5, RN10)
  Para no perder ni conservar indebidamente acceso a través de un marcador

  Background:
    Given that I am an authenticated user in the system

  Scenario Outline: Marcar como favorito según el tipo de acceso al recurso (RN5)
    Given that a resource of type "<tipo_recurso>" exists
    When I try to mark it as favorite
    Then the result of the action is "<resultado>"

    Examples:
      | tipo_recurso                   | resultado             |
      | público                        | marcado exitosamente  |
      | compartido conmigo              | marcado exitosamente  |
      | propio                          | marcado exitosamente  |
      | privado no compartido conmigo   | acción rechazada      |

  Scenario: Un recurso favorito pierde disponibilidad al revocarse el acceso compartido (RN10)
    Given that the resource "R2" is in my favorites list
    And the owner revokes the shared access to "R2"
    When I access my favorites list
    Then "R2" is no longer available to open
    And the system indicates that access was revoked
