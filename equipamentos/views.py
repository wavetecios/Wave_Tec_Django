from django.shortcuts import render
from clientes.models import Cliente


def novo_equipamento(request):

    clientes = Cliente.objects.all()

    return render(
        request,
        "equipamentos/novo_equipamento.html",
        {
            "clientes": clientes
        }
    )