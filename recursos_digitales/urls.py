from django.urls import path

from . import views

app_name = 'recursos_digitales'

urlpatterns = [
    path('', views.CatalogoListView.as_view(), name='catalogo'),
    path('nuevo/original/', views.RecursoOriginalCreateView.as_view(), name='crear_original'),
    path('nuevo/externo/', views.RecursoExternoCreateView.as_view(), name='crear_externo'),
    path('<int:pk>/', views.RecursoDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.RecursoUpdateView.as_view(), name='editar'),
]