# language: en
Feature: Compartir y revocar acceso a recursos educativos digitales
  Como propietario de un recurso
  Quiero compartir mis recursos con otros usuarios y revocar ese acceso cuando lo decida
  Para controlar quién puede ver mi contenido

  Background:
    Given that the users "Ana", "Luis" and "Marta" exist
    And the resource "Ejercicios de Álgebra Lineal" is private and belongs to Luis

  # --- Compartir ---

  Scenario: El propietario comparte un recurso con otro usuario
    When Luis shares "Ejercicios de Álgebra Lineal" with Ana
    Then Ana should have access to the resource "Ejercicios de Álgebra Lineal"
    And the resource should appear in Ana's "recursos compartidos conmigo" list

  Scenario: El propietario comparte un recurso con varios usuarios
    When Luis shares "Ejercicios de Álgebra Lineal" with Ana and Marta
    Then Ana should have access to the resource "Ejercicios de Álgebra Lineal"
    And Marta should have access to the resource "Ejercicios de Álgebra Lineal"

  Scenario: Un usuario que no es propietario no puede compartir el recurso
    When Ana attempts to share "Ejercicios de Álgebra Lineal" with Marta
    Then the system should reject the action
    And it should display a message indicating that only the owner can share the resource

  Scenario: Un usuario con quien se compartió un recurso no puede volver a compartirlo con otros
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Ana attempts to share "Ejercicios de Álgebra Lineal" with Marta
    Then the system should reject the action

  Scenario: Compartir un recurso que ya fue compartido con el mismo usuario no duplica el acceso
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Luis attempts to share "Ejercicios de Álgebra Lineal" again with Ana
    Then the system should not duplicate access
    And Ana should continue to have access to the resource

  # --- Revocar ---

  Scenario: El propietario revoca el acceso previamente otorgado
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Luis revokes Ana's access to "Ejercicios de Álgebra Lineal"
    Then Ana should no longer have access to the resource "Ejercicios de Álgebra Lineal"
    And the resource should not appear in Ana's "recursos compartidos conmigo" list

  Scenario: Un usuario que no es propietario no puede revocar el acceso de otro
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana and Marta
    When Marta attempts to revoke Ana's access to "Ejercicios de Álgebra Lineal"
    Then the system should reject the action
    And Ana should continue to have access to the resource

  Scenario: Revocar el acceso a un usuario que no tenía el recurso compartido no genera cambios
    When Luis attempts to revoke Marta's access to "Ejercicios de Álgebra Lineal"
    Then the system should not make any changes
    And it should indicate that Marta did not have access to the resource