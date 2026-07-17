from django.urls import path

from . import views

app_name = 'espacio_personal'

urlpatterns = [
    # Colecciones (característica 5)
    path('colecciones/', views.ColeccionListView.as_view(), name='coleccion_lista'),
    path('colecciones/nueva/', views.ColeccionCreateView.as_view(), name='coleccion_crear'),
    path('colecciones/<int:pk>/', views.ColeccionDetailView.as_view(), name='coleccion_detalle'),
    path('colecciones/<int:pk>/editar/', views.ColeccionUpdateView.as_view(), name='coleccion_editar'),
    path('colecciones/<int:pk>/eliminar/', views.ColeccionDeleteView.as_view(), name='coleccion_eliminar'),
    path(
        'colecciones/<int:coleccion_pk>/recurso/<int:recurso_pk>/toggle/',
        views.ColeccionRecursoToggleView.as_view(),
        name='coleccion_toggle_recurso',
    ),

    # Favoritos (característica 6)
    path('favoritos/', views.FavoritoListView.as_view(), name='favorito_lista'),
    path(
        'favoritos/<int:recurso_pk>/toggle/',
        views.FavoritoToggleView.as_view(),
        name='favorito_toggle',
    ),

    # Anotaciones (característica 7 / Regla 8) — siempre bajo un recurso puntual
    path('recursos/<int:recurso_pk>/notas/', views.AnotacionListView.as_view(), name='anotaciones'),
    path(
        'recursos/<int:recurso_pk>/notas/nueva/',
        views.AnotacionCreateView.as_view(),
        name='anotacion_crear',
    ),
    path('notas/<int:pk>/editar/', views.AnotacionUpdateView.as_view(), name='anotacion_editar'),
    path('notas/<int:pk>/eliminar/', views.AnotacionDeleteView.as_view(), name='anotacion_eliminar'),
]
