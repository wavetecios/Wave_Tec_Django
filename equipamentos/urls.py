from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.lista_equipamentos,
        name="lista_equipamentos"
    ),

    path(
        "novo/<int:cliente_id>/",
        views.novo_equipamento,
        name="novo_equipamento"
    ),

    path(
        "editar/<int:equipamento_id>/",
        views.editar_equipamento,
        name="editar_equipamento"
    ),

]