from django.shortcuts import render

from clientes.models import Cliente
from equipamentos.models import Equipamento
from ordens.models import OrdemServico


def home(request):

    total_clientes = Cliente.objects.count()
    total_equipamentos = Equipamento.objects.count()
    total_ordens = OrdemServico.objects.count()

    context = {
        "total_clientes": total_clientes,
        "total_equipamentos": total_equipamentos,
        "total_ordens": total_ordens,
    }

    return render(request, "core/home.html", context)