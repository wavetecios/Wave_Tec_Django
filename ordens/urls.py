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
        "<int:ordem_id>/",
        views.detalhe_ordem,
        name="detalhe_ordem"
    ),

    path(
        "imprimir/<int:ordem_id>/",
        views.imprimir_os,
        name="imprimir_os"
    ),

]
