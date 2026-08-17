from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("core.urls")
    ),

    path(
        "clientes/",
        include("clientes.urls")
    ),

    path(
        "equipamentos/",
        include("equipamentos.urls")
    ),

    path(
        "ordens/",
        include("ordens.urls")
    ),

    path(
        "atendimentos/",
        include("atendimentos.urls")
    ),

    path(
        "financeiro/",
        include("financeiro.urls")
    ),

    path(
        "pesquisa/",
        include("pesquisa.urls")
    ),

]