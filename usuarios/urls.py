from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tecnicos, name='lista_tecnicos'),
    path('novo/', views.novo_tecnico, name='novo_tecnico'),
    path('editar/<int:tecnico_id>/', views.editar_tecnico, name='editar_tecnico'),
    path('excluir/<int:tecnico_id>/', views.excluir_tecnico, name='excluir_tecnico'),
]
