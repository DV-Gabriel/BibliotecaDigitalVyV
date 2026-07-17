# language: en
Feature: Acceder a recursos compartidos por otros usuarios
  Como usuario
  Quiero ver y consultar los recursos que otros usuarios han compartido conmigo
  Para aprovechar el material que me ha sido otorgado

  Background:
    Given that the users "Ana", "Luis" and "Marta" exist
    And the resource "Ejercicios de Álgebra Lineal" is private and belongs to Luis
    And the resource "Apuntes de Química Orgánica" is private and belongs to Marta

  Scenario: Un usuario ve en su lista solo los recursos compartidos con él
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Ana checks her "recursos compartidos conmigo" list
    Then she should see the resource "Ejercicios de Álgebra Lineal" in the list
    And she should not see the resource "Apuntes de Química Orgánica" in the list

  Scenario: Un usuario puede abrir y consultar el contenido de un recurso compartido con él
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Ana opens the resource "Ejercicios de Álgebra Lineal"
    Then she should be able to view its full content

  Scenario: Un usuario no puede acceder a un recurso privado que no le ha sido compartido
    When Ana attempts to open the resource "Apuntes de Química Orgánica"
    Then the system should deny access
    And it should display a message indicating that she does not have permission to view that resource

  Scenario: Un usuario puede acceder a un recurso compartido con varios usuarios a la vez
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana and Marta
    When Marta opens the resource "Ejercicios de Álgebra Lineal"
    Then she should be able to view its full content

  Scenario: Cualquier usuario puede acceder a un recurso público sin necesidad de que se lo compartan
    Given that the user "Carlos" exists
    And the resource "Introducción a la Física" is public and belongs to Carlos
    When Ana opens the resource "Introducción a la Física"
    Then she should be able to view its full content

  Scenario: Un usuario con acceso compartido no puede modificar el recurso
    Given that "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Ana attempts to edit the resource "Ejercicios de Álgebra Lineal"
    Then the system should reject the action
    And it should display a message indicating that only the owner can modify the resource