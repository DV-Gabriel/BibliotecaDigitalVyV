Característica: Gestionar favoritos y marcadores de acceso rápido
Como estudiante o docente
Quiero marcar y desmarcar recursos como favoritos
Para acceder rápidamente a los recursos que más utilizo

Antecedentes:
Dado que soy un usuario autenticado en el sistema
Y existe un catálogo de recursos educativos digitales

Esquema del escenario: Intentar marcar como favorito según el tipo de acceso al recurso
Dado que existe un recurso de tipo "<tipo_recurso>"
Cuando intento marcarlo como favorito
Entonces el resultado de la acción es "<resultado>"

Ejemplos:
| tipo_recurso                        | resultado                    |
| público                             | marcado exitosamente         |
| compartido conmigo                  | marcado exitosamente         |
| propio                              | marcado exitosamente         |
| privado no compartido conmigo       | acción rechazada             |
| compartido y luego revocado         | eliminado automáticamente de favoritos |

Escenario: Intentar marcar un recurso ya marcado como favorito
Dado que el recurso "R1" ya está en mi lista de favoritos
Cuando intento marcar nuevamente "R1" como favorito
Entonces el sistema no genera un duplicado
Y me indica que el recurso ya se encuentra en favoritos

Escenario: Quitar un recurso de favoritos
Dado que el recurso "R1" está en mi lista de favoritos
Cuando selecciono la opción "Quitar de favoritos" sobre "R1"
Entonces "R1" deja de aparecer en mi lista de favoritos

Escenario: Visualizar la lista de favoritos
Dado que tengo varios recursos marcados como favoritos
Cuando accedo a la sección "Mis favoritos"
Entonces veo el listado completo de recursos marcados
Ordenados por fecha de marcado más reciente

Escenario: Un recurso favorito pierde el acceso compartido
Dado que el recurso "R2" está en mi lista de favoritos
Y el propietario revoca el acceso compartido sobre "R2"
Cuando accedo a mi lista de favoritos
Entonces "R2" ya no está disponible para abrir
Y el sistema indica que el acceso fue revocado

Escenario: Acceso rápido desde un marcador de favorito
Dado que tengo el recurso "R1" marcado como favorito
Cuando hago clic sobre "R1" desde la sección de favoritos
Entonces soy redirigido directamente a la vista del recurso

