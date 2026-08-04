from django.shortcuts import render, redirect, get_object_or_404

from .models import OrdemServico
from equipamentos.models import Equipamento


def lista_ordens(request):

    ordens = OrdemServico.objects.all().order_by("-id")

    return render(
        request,
        "ordens/lista_ordens.html",
        {
            "ordens": ordens
        }
    )


def nova_ordem(request, equipamento_id):

    equipamento = get_object_or_404(
        Equipamento,
        id=equipamento_id
    )

    cliente = equipamento.cliente

    if request.method == "POST":

        acessorios = equipamento.acessorios
        defeito = request.POST["defeito"]
        observacoes = request.POST["observacoes"]

        OrdemServico.objects.create(

            equipamento_cadastrado=equipamento,

            defeito=defeito,

            acessorios=acessorios,

            observacoes=observacoes

        )

        print("ORDEM SALVA")

        return redirect("lista_ordens")

    return render(
        request,
        "ordens/nova_ordem.html",
        {
            "cliente": cliente,
            "equipamento": equipamento,
        }
    )


def imprimir_os(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    atendimento = getattr(
        ordem,
        "atendimento",
        None
    )

    return render(
        request,
        "ordens/imprimir_os.html",
        {
            "ordem": ordem,
            "cliente": ordem.cliente,
            "equipamento": ordem.equipamento_cadastrado,
            "atendimento": atendimento,
        }
    )