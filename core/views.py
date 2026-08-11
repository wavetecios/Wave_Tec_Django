from django.shortcuts import render

from clientes.models import Cliente
from equipamentos.models import Equipamento
from ordens.models import OrdemServico


def home(request):

    total_clientes = Cliente.objects.count()
    total_equipamentos = Equipamento.objects.count()
    total_ordens = OrdemServico.objects.count()

    ordens_abertas = OrdemServico.objects.filter(
        status="ABERTA"
    ).count()

    ordens_analise = OrdemServico.objects.filter(
        status="EM_ANALISE"
    ).count()

    ordens_reparo = OrdemServico.objects.filter(
        status="EM_REPARO"
    ).count()

    ordens_prontas = OrdemServico.objects.filter(
        status="PRONTO"
    ).count()

    ordens_entregues = OrdemServico.objects.filter(
        status="ENTREGUE"
    ).count()

    context = {

        "total_clientes": total_clientes,
        "total_equipamentos": total_equipamentos,
        "total_ordens": total_ordens,

        "ordens_abertas": ordens_abertas,
        "ordens_analise": ordens_analise,
        "ordens_reparo": ordens_reparo,
        "ordens_prontas": ordens_prontas,
        "ordens_entregues": ordens_entregues,

    }

    return render(
        request,
        "core/home.html",
        context
    )