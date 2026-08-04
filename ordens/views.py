from django.shortcuts import render, redirect

from .models import OrdemServico
from equipamentos.models import Equipamento


def lista_ordens(request):

    ordens = OrdemServico.objects.all()

    return render(
        request,
        "ordens/lista_ordens.html",
        {
            "ordens": ordens
        }
    )


def nova_ordem(request, equipamento_id):

    equipamento = Equipamento.objects.get(id=equipamento_id)

    cliente = equipamento.cliente

    if request.method == "POST":

        defeito = request.POST["defeito"]
        observacoes = request.POST["observacoes"]

        OrdemServico.objects.create(

            equipamento_cadastrado=equipamento,

            defeito=defeito,

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