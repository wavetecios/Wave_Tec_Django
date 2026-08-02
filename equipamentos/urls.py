from django.urls import path
from . import views

urlpatterns = [

    path("", views.lista_equipamentos, name="lista_equipamentos"),
    path("novo/", views.novo_equipamento, name="novo_equipamento"),
]