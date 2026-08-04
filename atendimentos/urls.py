from django.urls import path

from . import views


urlpatterns = [

    path(
        "novo/<int:ordem_id>/",
        views.novo_atendimento,
        name="novo_atendimento",
    ),

]