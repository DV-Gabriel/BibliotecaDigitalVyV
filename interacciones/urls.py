from django.urls import path

from . import views

app_name = 'interacciones'

urlpatterns = [
    path(
        'recursos/<int:recurso_pk>/compartir/',
        views.CompartirRecursoView.as_view(),
        name='compartir',
    ),
    path(
        'recursos/<int:recurso_pk>/compartidos/',
        views.CompartidosPorRecursoListView.as_view(),
        name='compartidos_por_recurso',
    ),
    path('compartidos/<int:pk>/revocar/', views.RevocarAccesoView.as_view(), name='revocar'),
    path(
        'compartido-conmigo/',
        views.RecursosCompartidosConmigoListView.as_view(),
        name='compartidos_conmigo',
    ),
]
