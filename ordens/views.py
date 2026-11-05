from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from usuarios.decorators import tecnico_required, admin_required
from .models import OrdemServico
from equipamentos.models import Equipamento
from financeiro.models import Lancamento
from atendimentos.models import Atendimento
from django.core.exceptions import ValidationError
from django.db import models


def _sync_finance_from_ordem(ordem):
    atendimento = getattr(ordem, "atendimento", None)
    if ordem.status == "ENTREGUE":
        valor = atendimento.valor if atendimento else ordem.valor
        if valor and valor > 0:
            Lancamento.objects.update_or_create(
                ordem=ordem,
                defaults={
                    "tipo": "RECEITA",
                    "categoria": "SERVICOS",
                    "descricao": f"OS #{ordem.id} - {ordem.cliente.nome}",
                    "valor": valor,
                    "forma_pagamento": ordem.forma_pagamento or "DINHEIRO",
                    "observacoes": "Receita gerada automaticamente após entrega da ordem.",
                },
            )
            return
    Lancamento.objects.filter(ordem=ordem).delete()


@login_required
@tecnico_required
def lista_ordens(request):

    status = request.GET.get("status")

    ordens = OrdemServico.objects.all()

    if status:

        ordens = ordens.filter(
            status=status
        )

    ordens = ordens.order_by("-id")

    return render(

        request,

        "ordens/lista_ordens.html",

        {

            "ordens": ordens,
            "status_filtro": status,

        }

    )


@login_required
@tecnico_required
def nova_ordem(request, equipamento_id):

    equipamento = get_object_or_404(
        Equipamento,
        id=equipamento_id
    )

    cliente = equipamento.cliente

    if request.method == "POST":

        defeito = request.POST["defeito"]
        observacoes = request.POST["observacoes"]

        OrdemServico.objects.create(

            equipamento_cadastrado=equipamento,

            defeito=defeito,

            acessorios=equipamento.acessorios,

            observacoes=observacoes

        )

        return redirect("lista_ordens")

    return render(

        request,

        "ordens/nova_ordem.html",

        {

            "cliente": cliente,
            "equipamento": equipamento,

        }

    )


@login_required
@admin_required
def editar_ordem(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    if request.method == "POST":

        ordem.defeito = request.POST["defeito"]
        ordem.acessorios = request.POST["acessorios"]
        ordem.observacoes = request.POST["observacoes"]

        pagamento = request.POST.get("forma_pagamento", "").strip()
        if pagamento in {"DINHEIRO", "PIX", "CARTAO", "TRANSFERENCIA"}:
            ordem.forma_pagamento = pagamento

        status = request.POST.get("status", "").strip()
        if status in dict(OrdemServico.STATUS):
            ordem.status = status

        ordem.save()

        atendimento = getattr(ordem, "atendimento", None)
        if atendimento:
            atendimento.forma_pagamento = ordem.forma_pagamento
            atendimento.status = ordem.status
            atendimento.save()
            if ordem.status == "ENTREGUE" and atendimento.valor > 0:
                atendimento.valor = atendimento.valor
                atendimento.save()

        _sync_finance_from_ordem(ordem)

        return redirect("lista_ordens")

    return render(

        request,

        "ordens/editar_ordem.html",

        {

            "ordem": ordem,
            "cliente": ordem.cliente,
            "equipamento": ordem.equipamento_cadastrado,

        }

    )


@login_required
@tecnico_required
def detalhe_ordem(request, ordem_id):

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

        "ordens/detalhe_ordem.html",

        {

            "ordem": ordem,
            "cliente": ordem.cliente,
            "equipamento": ordem.equipamento_cadastrado,
            "atendimento": atendimento,

        }

    )


@login_required
@tecnico_required
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


@login_required
@tecnico_required
def imprimir_entrada(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    return render(
        request,
        "ordens/imprimir_entrada_a5.html",
        {
            "ordem": ordem,
            "cliente": ordem.cliente,
            "equipamento": ordem.equipamento_cadastrado,
        }
    )


@login_required
@admin_required
def finalizar_ordem(request, ordem_id):

    ordem = get_object_or_404(
        OrdemServico,
        id=ordem_id
    )

    if request.method == "POST":

        pagamento = request.POST.get("forma_pagamento", "").strip()
        if pagamento in {"DINHEIRO", "PIX", "CARTAO", "TRANSFERENCIA"}:
            ordem.forma_pagamento = pagamento

        status = request.POST.get("status", "").strip()
        if status in dict(OrdemServico.STATUS):
            ordem.status = status

        valor = request.POST.get("valor", "").strip()
        try:
            ordem.valor = Decimal(valor) if valor else Decimal("0.00")
        except InvalidOperation:
            ordem.valor = Decimal("0.00")

        ordem.save()

        atendimento = getattr(ordem, "atendimento", None)
        if atendimento:
            atendimento.forma_pagamento = ordem.forma_pagamento
            atendimento.status = ordem.status
            atendimento.valor = ordem.valor
            atendimento.save()
            if ordem.status == "ENTREGUE" and atendimento.valor > 0:
                atendimento.valor = atendimento.valor
                atendimento.save()

        _sync_finance_from_ordem(ordem)

        return redirect("lista_ordens")

    return render(
        request,
        "ordens/finalizar_ordem.html",
        {
            "ordem": ordem,
            "cliente": ordem.cliente,
            "equipamento": ordem.equipamento_cadastrado,
        }
    )

