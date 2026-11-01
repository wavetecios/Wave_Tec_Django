from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from usuarios.decorators import tecnico_required
from .models import Atendimento
from ordens.models import OrdemServico
from financeiro.models import Lancamento


def _is_admin(user):
    tecnico = getattr(user, "tecnico", None)
    return user.is_superuser or (
        tecnico is not None and tecnico.ativo and tecnico.perfil == "ADMIN"
    )


def _sync_finance_por_entrega(atendimento, ordem):
    status_map = {
        "ABERTA": "ABERTA",
        "EM_ANALISE": "EM_ANALISE",
        "AGUARDANDO_PECA": "AGUARDANDO_PECA",
        "EM_REPARO": "EM_REPARO",
        "PRONTO": "PRONTO",
        "SEM_CONSERTO": "SEM_CONSERTO",
        "ENTREGUE": "ENTREGUE",
    }

    if atendimento.status in status_map:
        ordem.status = status_map[atendimento.status]

    if atendimento.status == "ENTREGUE" and atendimento.valor > Decimal("0.00"):
        ordem.valor = atendimento.valor
        ordem.forma_pagamento = atendimento.forma_pagamento or "DINHEIRO"
        ordem.save()

        Lancamento.objects.update_or_create(
            ordem=ordem,
            defaults={
                "tipo": "RECEITA",
                "categoria": "SERVICOS",
                "descricao": f"OS #{ordem.id} - {ordem.cliente.nome}",
                "valor": atendimento.valor,
                "forma_pagamento": atendimento.forma_pagamento or "DINHEIRO",
                "observacoes": "Receita gerada automaticamente após a entrega da ordem.",
            },
        )
        return

    ordem.valor = atendimento.valor
    ordem.forma_pagamento = ""
    ordem.save()
    Lancamento.objects.filter(ordem=ordem).delete()


@login_required
@tecnico_required
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

        if _is_admin(request.user):
            pagamento = request.POST.get("forma_pagamento", "").strip()
            if pagamento in {"DINHEIRO", "PIX", "CARTAO", "TRANSFERENCIA"}:
                atendimento.forma_pagamento = pagamento

            status = request.POST.get("status", "").strip()
            if status in dict(Atendimento.STATUS):
                atendimento.status = status

        atendimento.save()
        _sync_finance_por_entrega(atendimento, ordem)

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
@tecnico_required
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

        if _is_admin(request.user):
            pagamento = request.POST.get("forma_pagamento", "").strip()
            if pagamento in {"DINHEIRO", "PIX", "CARTAO", "TRANSFERENCIA"}:
                atendimento.forma_pagamento = pagamento

            status = request.POST.get("status", "").strip()
            if status in dict(Atendimento.STATUS):
                atendimento.status = status

        atendimento.save()
        _sync_finance_por_entrega(atendimento, ordem)

        return redirect("lista_ordens")

    return render(
        request,
        "atendimentos/editar_atendimento.html",
        {
            "ordem": ordem,
            "atendimento": atendimento,
        }
    )