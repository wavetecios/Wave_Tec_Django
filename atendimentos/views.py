from django.shortcuts import render, redirect, get_object_or_404

from .models import Atendimento
from ordens.models import OrdemServico


def novo_atendimento(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    atendimento, criado = Atendimento.objects.get_or_create(
        ordem=ordem
    )

    if request.method == "POST":

        atendimento.diagnostico = request.POST["diagnostico"]
        atendimento.servico_executado = request.POST["servico_executado"]
        atendimento.pecas_utilizadas = request.POST["pecas_utilizadas"]
        atendimento.valor = request.POST["valor"]
        atendimento.forma_pagamento = request.POST["forma_pagamento"]
        atendimento.status = request.POST["status"]

        atendimento.save()

        mapa_status = {
            "EM_ANALISE": "EM_ANALISE",
            "EM_REPARO": "EM_REPARO",
            "PRONTO": "PRONTO",
            "ENTREGUE": "ENTREGUE",
            "AGUARDANDO_PECA": "AGUARDANDO_PECA",
            "SEM_CONSERTO": "SEM_CONSERTO",
        }

        if atendimento.status in mapa_status:
            ordem.status = mapa_status[atendimento.status]
            ordem.save()

        return redirect("lista_ordens")

    return render(
        request,
        "atendimentos/novo_atendimento.html",
        {
            "ordem": ordem,
            "atendimento": atendimento,
        }
    )


def editar_atendimento(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    atendimento = get_object_or_404(
        Atendimento,
        ordem=ordem
    )

    if request.method == "POST":

        atendimento.diagnostico = request.POST["diagnostico"]
        atendimento.servico_executado = request.POST["servico_executado"]
        atendimento.pecas_utilizadas = request.POST["pecas_utilizadas"]
        atendimento.valor = request.POST["valor"]
        atendimento.forma_pagamento = request.POST["forma_pagamento"]
        atendimento.status = request.POST["status"]

        atendimento.save()

        ordem.status = atendimento.status
        ordem.save()

        return redirect("lista_ordens")

    return render(
        request,
        "atendimentos/editar_atendimento.html",
        {
            "ordem": ordem,
            "atendimento": atendimento,
        }
    )