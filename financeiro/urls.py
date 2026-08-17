from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.lista_financeiro,
        name="lista_financeiro"
    ),

    path(
        "novo/",
        views.novo_lancamento,
        name="novo_lancamento"
    ),

    path(
        "editar/<int:lancamento_id>/",
        views.editar_lancamento,
        name="editar_lancamento"
    ),


    path(
    "excluir/<int:lancamento_id>/",
    views.excluir_lancamento,
    name="excluir_lancamento"

    ),

]