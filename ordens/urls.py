from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.lista_ordens,
        name="lista_ordens"
    ),

    path(
        "nova/<int:equipamento_id>/",
        views.nova_ordem,
        name="nova_ordem"
    ),

    path(
        "editar/<int:ordem_id>/",
        views.editar_ordem,
        name="editar_ordem"
    ),

    path(
        "imprimir/<int:ordem_id>/",
        views.imprimir_os,
        name="imprimir_os"
    ),

    path(
    "entrada/<int:ordem_id>/",
    views.imprimir_entrada,
    name="imprimir_entrada"
    ), 

    path(
        "finalizar/<int:ordem_id>/",
        views.finalizar_ordem,
        name="finalizar_ordem"
    ),

    # SEMPRE deixe a rota genérica por último
    path(
        "<int:ordem_id>/",
        views.detalhe_ordem,
        name="detalhe_ordem"
    ),

]