from django.shortcuts import render
from .models import OrdemServico

def lista_ordens(request):
    ordens = OrdemServico.objects.all()

    return render(
        request,
        "ordens/lista_ordens.html",
        {"ordens": ordens}
    )

def nova_ordem(request):

    return render(
        request,
        "ordens/nova_ordem.html"
    )