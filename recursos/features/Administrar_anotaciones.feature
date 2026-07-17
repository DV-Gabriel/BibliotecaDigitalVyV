# language: en
Feature: Administrar anotaciones y notas personales por recurso
  Como usuario
  Quiero registrar anotaciones personales sobre los recursos educativos
  Para guardar información importante relacionada con mi aprendizaje

  Background:
    Given that I am an authenticated user in the system
    And I have access to the resource I want to annotate

  Scenario Outline: Crear una anotación personal según el tipo de acceso al recurso
    Given that I have "<tipo_acceso>" access to the resource "<recurso>"
    When I add a personal annotation about "<recurso>"
    Then the annotation is saved and associated only to my user
    And it is not visible to any other user who views "<recurso>"

    Examples:
      | tipo_acceso | recurso |
      | propio      | R1      |
      | público     | R2      |
      | compartido  | R3      |

  Scenario: Editar una anotación propia
    Given that I have a previous annotation on resource "R1"
    When I change the content of that annotation
    Then the new content is saved
    And its private nature is preserved

  Scenario: Eliminar una anotación propia
    Given that I have an annotation registered on resource "R1"
    When I delete that annotation
    Then the annotation is no longer associated with the resource
    And it no longer appears in my notes list for "R1"

  Scenario: Consultar mis anotaciones sobre un recurso
    Given that I have created one or more annotations on resource "R1"
    When I open the annotations view for "R1"
    Then I see only the annotations that I myself created

  Scenario: Otro usuario no puede ver mis anotaciones en un recurso compartido
    Given that I share resource "R1" with another user
    And I have personal annotations on "R1"
    When the other user opens "R1"
    Then they do not see any of my annotations

  Scenario: Intentar anotar un recurso al que perdí el acceso
    Given that my access to resource "R3" was revoked by its owner
    When I try to add an annotation about "R3"
    Then the system rejects the action
    And it indicates that I no longer have access to the resource

  Scenario: Las anotaciones existentes permanecen ocultas tras revocar el acceso
    Given that I had annotations on resource "R3"
    And the owner revokes my access to "R3"
    When I try to view my previous annotations for "R3"
    Then the system does not allow me to view them while I do not have access to the resource

  Scenario Outline: Visibilidad de anotaciones según el tipo de usuario que consulta el recurso
    Given that the user "<usuario_creador>" creates an annotation on a resource
    When the user "<usuario_consultor>" opens that same resource
    Then the annotation is "<visibilidad>"

    Examples:
      | usuario_creador | usuario_consultor             | visibilidad |
      | propietario     | propietario (él mismo)        | visible     |
      | propietario     | usuario con acceso compartido | no visible  |
      | invitado        | propietario del recurso       | no visible  |
      | invitado        | invitado (él mismo)           | visible     |
      | invitado        | otro invitado con acceso      | no visible  |