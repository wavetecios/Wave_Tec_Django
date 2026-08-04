from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista_ordens, name="lista_ordens"),

    path(
        "nova/<int:equipamento_id>/",
        views.nova_ordem,
        name="nova_ordem"
    ),

]