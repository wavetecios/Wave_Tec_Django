from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from usuarios.decorators import tecnico_required, admin_required
from .models import OrdemServico
from equipamentos.models import Equipamento


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

        ordem.save()

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

