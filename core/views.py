from decimal import Decimal

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from clientes.models import Cliente
from equipamentos.models import Equipamento
from ordens.models import OrdemServico
from financeiro.models import Lancamento


def home(request):

    hoje = timezone.localdate()

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


    # ==============================
    # FINANCEIRO - MÊS ATUAL
    # ==============================

    lancamentos_mes = Lancamento.objects.filter(
        data__year=hoje.year,
        data__month=hoje.month
    )


    receitas_mes = (
        lancamentos_mes
        .filter(tipo="RECEITA")
        .aggregate(
            total=Sum("valor")
        )["total"]
        or Decimal("0.00")
    )


    despesas_mes = (
        lancamentos_mes
        .filter(tipo="DESPESA")
        .aggregate(
            total=Sum("valor")
        )["total"]
        or Decimal("0.00")
    )


    saldo_mes = receitas_mes - despesas_mes


    context = {

        "total_clientes": total_clientes,

        "total_equipamentos": total_equipamentos,

        "total_ordens": total_ordens,

        "ordens_abertas": ordens_abertas,

        "ordens_analise": ordens_analise,

        "ordens_reparo": ordens_reparo,

        "ordens_prontas": ordens_prontas,

        "ordens_entregues": ordens_entregues,

        "receitas_mes": receitas_mes,

        "despesas_mes": despesas_mes,

        "saldo_mes": saldo_mes,

    }


    return render(
        request,
        "core/home.html",
        context
    )