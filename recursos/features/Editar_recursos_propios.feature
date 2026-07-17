# language: en
Feature: Editar mis propios recursos educativos digitales (Actualizar recursos propios)
  Como usuario
  Quiero modificar la información de los recursos que he creado
  Para mantener el contenido actualizado y corregir posibles errores

  Background:
    Given that the users "Ana", "Luis" and "Marta" exist
    And the user "Luis" is authenticated in the system
    And "Luis" has created the resource "Apuntes de Álgebra" with:
      | campo       | valor               |
      | descripción | Resumen de vectores |
      | categoría   | Matemáticas         |
      | etiquetas   | vectores, álgebra   |
      | autor       | Luis                |

  Scenario: Editar el título y la descripción de un recurso propio
    When the user changes the resource title to "Apuntes de Álgebra Lineal"
    And changes the description to "Resumen detallado de vectores y matrices"
    Then the resource should be updated with the new title and description
    And Luis should remain the owner of the resource

  Scenario: Cambiar la categoría de un recurso propio
    When the user changes the resource category to "Ciencias Exactas"
    Then the resource should show the new category "Ciencias Exactas"

  Scenario: Actualizar etiquetas de un recurso propio
    When the user adds the tag "matrices" to the resource
    And removes the tag "vectores"
    Then the resource should have the tags "álgebra" and "matrices"

  Scenario: Cambiar el autor (externo) de un recurso propio
    When the user changes the resource author to "Autor Externo de Referencia"
    Then the resource should show the new author "Autor Externo de Referencia"

  Scenario: Un usuario no puede editar un recurso que no ha creado
    Given that "Ana" created the resource "Guía de Biología"
    When Luis attempts to edit the resource "Guía de Biología"
    Then the system should reject the action
    And it should display a message indicating that only the owner can edit the resource

  Scenario Outline: No permitir dejar campos obligatorios vacíos al editar
    When the user attempts "<accion>" on the resource "Apuntes de Álgebra"
    Then the system should prevent saving the changes
    And it should indicate "<mensaje>"

    Examples:
      | accion                       | mensaje                                     |
      | borrar el título             | el título es obligatorio                    |
      | borrar la descripción        | la descripción es obligatoria               |
      | quitar todas las etiquetas   | el recurso debe tener al menos una etiqueta |
      | desvincular la categoría     | la categoría es obligatoria                 |