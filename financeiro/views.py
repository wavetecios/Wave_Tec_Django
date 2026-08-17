from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Lancamento


def lista_financeiro(request):

    hoje = timezone.localdate()

    periodo = request.GET.get("periodo", "mes")

    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")

    lancamentos = Lancamento.objects.all()

    if periodo == "hoje":

        lancamentos = lancamentos.filter(
            data=hoje
        )

    elif periodo == "mes":

        lancamentos = lancamentos.filter(
            data__year=hoje.year,
            data__month=hoje.month
        )

    elif periodo == "ano":

        lancamentos = lancamentos.filter(
            data__year=hoje.year
        )

    elif periodo == "personalizado":

        if data_inicio:
            lancamentos = lancamentos.filter(
                data__gte=data_inicio
            )

        if data_fim:
            lancamentos = lancamentos.filter(
                data__lte=data_fim
            )

    lancamentos = lancamentos.order_by(
        "-data",
        "-id"
    )

    total_receitas = sum(
        (
            lancamento.valor
            for lancamento in lancamentos
            if lancamento.tipo == "RECEITA"
        ),
        Decimal("0.00")
    )

    total_despesas = sum(
        (
            lancamento.valor
            for lancamento in lancamentos
            if lancamento.tipo == "DESPESA"
        ),
        Decimal("0.00")
    )

    saldo = total_receitas - total_despesas

    return render(
        request,
        "financeiro/lista_financeiro.html",
        {
            "lancamentos": lancamentos,
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": saldo,
            "periodo": periodo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }
    )


def novo_lancamento(request):

    if request.method == "POST":

        Lancamento.objects.create(
            tipo=request.POST["tipo"],
            descricao=request.POST["descricao"],
            valor=request.POST["valor"],
            forma_pagamento=request.POST["forma_pagamento"],
            observacoes=request.POST["observacoes"]
        )

        return redirect("lista_financeiro")

    return render(
        request,
        "financeiro/novo_lancamento.html"
    )


def editar_lancamento(request, lancamento_id):

    lancamento = get_object_or_404(
        Lancamento,
        id=lancamento_id
    )

    if request.method == "POST":

        lancamento.tipo = request.POST["tipo"]
        lancamento.descricao = request.POST["descricao"]
        lancamento.valor = request.POST["valor"]
        lancamento.forma_pagamento = request.POST["forma_pagamento"]
        lancamento.observacoes = request.POST["observacoes"]

        lancamento.save()

        return redirect("lista_financeiro")

    return render(
        request,
        "financeiro/editar_lancamento.html",
        {
            "lancamento": lancamento
        }
    )


def excluir_lancamento(request, lancamento_id):

    lancamento = get_object_or_404(
        Lancamento,
        id=lancamento_id
    )

    if request.method == "POST":

        lancamento.delete()

        return redirect("lista_financeiro")

    return render(
        request,
        "financeiro/excluir_lancamento.html",
        {
            "lancamento": lancamento
        }
    )