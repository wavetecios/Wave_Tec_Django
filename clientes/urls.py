from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.lista_clientes,
        name="lista_clientes"
    ),

    path(
        "<int:cliente_id>/",
        views.detalhe_cliente,
        name="detalhe_cliente"
    ),

    path(
        "novo/",
        views.novo_cliente,
        name="novo_cliente"
    ),

    path(
        "editar/<int:cliente_id>/",
        views.editar_cliente,
        name="editar_cliente"
    ),

]