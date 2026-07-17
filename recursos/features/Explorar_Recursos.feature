# language: en
Feature: Explorar y buscar recursos digitales en el catálogo
  Como usuario
  Quiero que el catálogo me muestre únicamente los recursos a los que tengo acceso (RN5)
  Para encontrar material de mi interés sin exponer contenido privado de otros usuarios

  Background:
    Given that the following resources exist in the system:
      | titulo                       | visibilidad | propietario |
      | Introducción a la Física     | publico     | Carlos      |
      | Cálculo Diferencial          | publico     | Ana         |
      | Apuntes de Química Orgánica  | privado     | Marta       |
      | Ejercicios de Álgebra Lineal | compartido  | Luis        |

  Scenario: Un recurso privado no aparece en la búsqueda de otro usuario
    When Ana searches for "Química Orgánica" in the catalog
    Then she should not see the resource "Apuntes de Química Orgánica" in the results

  Scenario: Un recurso público sí aparece para cualquier usuario
    When Ana searches for "Física" in the catalog
    Then she should see the resource "Introducción a la Física" in the results

  Scenario: Un recurso compartido aparece solo para el usuario con quien fue compartido
    Given that the resource "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Ana searches for "Álgebra Lineal" in the catalog
    Then she should see the resource "Ejercicios de Álgebra Lineal" in the results

  Scenario: Un recurso compartido no aparece para un usuario ajeno al que se compartió
    Given that the resource "Ejercicios de Álgebra Lineal" was shared by Luis with Ana
    When Marta searches for "Álgebra Lineal" in the catalog
    Then she should not see the resource "Ejercicios de Álgebra Lineal" in the results

  Scenario Outline: Mostrar el rol del autor como indicador de confianza
    Given that the resource "<recurso>" has as author a user with role "<rol>"
    When Ana views the resource "<recurso>"
    Then she should see that the author has the role "<rol>"

    Examples:
      | recurso                    | rol         |
      | Introducción a la Física   | docente     |
      | Apuntes de clase de Luis   | estudiante  |

  Scenario: No mostrar rol cuando el autor es externo
    Given that the resource "Principios de Economía" has external author "Adam Smith"
    When Ana views the resource "Principios de Economía"
    Then the system should not display any role associated with the author
