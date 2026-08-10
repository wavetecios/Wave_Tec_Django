from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.pesquisa_global,
        name="pesquisa_global"
    ),

]