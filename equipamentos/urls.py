from django.urls import path
from . import views

urlpatterns = [
    path("novo/", views.novo_equipamento, name="novo_equipamento"),
]