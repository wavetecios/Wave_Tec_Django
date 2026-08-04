from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    
    path("clientes/", include("clientes.urls")),
    path("ordens/", include("ordens.urls")),
    path("equipamentos/", include("equipamentos.urls")),
     path("atendimentos/", include("atendimentos.urls")),
]