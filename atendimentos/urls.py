from django.urls import path

from . import views

urlpatterns = [

    path(
        "novo/<int:ordem_id>/",
        views.novo_atendimento,
        name="novo_atendimento",
    ),

    path(
        "editar/<int:ordem_id>/",
        views.editar_atendimento,
        name="editar_atendimento",
    ),

]