from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Atendimento
from ordens.models import OrdemServico
from financeiro.models import Lancamento


@login_required
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

        valor = request.POST.get("valor", "").strip()

        try:
            atendimento.valor = (
                Decimal(valor)
                if valor
                else Decimal("0.00")
            )
        except InvalidOperation:
            atendimento.valor = Decimal("0.00")

        atendimento.forma_pagamento = request.POST["forma_pagamento"]
        atendimento.status = request.POST["status"]

        atendimento.save()

        mapa_status = {

            "EM_ANALISE": "EM_ANALISE",
            "AGUARDANDO_PECA": "AGUARDANDO_PECA",
            "EM_REPARO": "EM_REPARO",
            "PRONTO": "PRONTO",
            "SEM_CONSERTO": "SEM_CONSERTO",
            "ENTREGUE": "ENTREGUE",

        }

        if atendimento.status in mapa_status:

            ordem.status = mapa_status[atendimento.status]

            ordem.save()

        if (
            atendimento.status == "ENTREGUE"
            and atendimento.valor > Decimal("0.00")
        ):

            Lancamento.objects.update_or_create(

                ordem=ordem,

                defaults={

                    "tipo": "RECEITA",

                    "categoria": "SERVICOS",

                    "descricao": (
                        f"OS #{ordem.id} - "
                        f"{ordem.cliente.nome}"
                    ),

                    "valor": atendimento.valor,

                    "forma_pagamento": (
                        atendimento.forma_pagamento
                    ),

                    "observacoes": (
                        "Receita gerada automaticamente "
                        "pela Ordem de Serviço."
                    ),

                }

            )

        else:

            Lancamento.objects.filter(
                ordem=ordem
            ).delete()

        return redirect("lista_ordens")

    return render(
        request,
        "atendimentos/novo_atendimento.html",
        {
            "ordem": ordem,
            "atendimento": atendimento,
        }
    )


@login_required
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

        valor = request.POST.get("valor", "").strip()

        try:
            atendimento.valor = (
                Decimal(valor)
                if valor
                else Decimal("0.00")
            )
        except InvalidOperation:
            atendimento.valor = Decimal("0.00")

        atendimento.forma_pagamento = request.POST["forma_pagamento"]
        atendimento.status = request.POST["status"]

        atendimento.save()

        mapa_status = {

            "EM_ANALISE": "EM_ANALISE",
            "AGUARDANDO_PECA": "AGUARDANDO_PECA",
            "EM_REPARO": "EM_REPARO",
            "PRONTO": "PRONTO",
            "SEM_CONSERTO": "SEM_CONSERTO",
            "ENTREGUE": "ENTREGUE",

        }

        if atendimento.status in mapa_status:

            ordem.status = mapa_status[atendimento.status]

            ordem.save()

        if (
            atendimento.status == "ENTREGUE"
            and atendimento.valor > Decimal("0.00")
        ):

            Lancamento.objects.update_or_create(

                ordem=ordem,

                defaults={

                    "tipo": "RECEITA",

                    "categoria": "SERVICOS",

                    "descricao": (
                        f"OS #{ordem.id} - "
                        f"{ordem.cliente.nome}"
                    ),

                    "valor": atendimento.valor,

                    "forma_pagamento": (
                        atendimento.forma_pagamento
                    ),

                    "observacoes": (
                        "Receita gerada automaticamente "
                        "pela Ordem de Serviço."
                    ),

                }

            )

        else:

            Lancamento.objects.filter(
                ordem=ordem
            ).delete()

        return redirect("lista_ordens")

    return render(
        request,
        "atendimentos/editar_atendimento.html",
        {
            "ordem": ordem,
            "atendimento": atendimento,
        }
    )