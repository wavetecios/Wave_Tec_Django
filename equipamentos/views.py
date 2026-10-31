from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from clientes.models import Cliente
from .models import Equipamento


@login_required
def lista_equipamentos(request):

    equipamentos = Equipamento.objects.all()

    return render(
        request,
        "equipamentos/lista_equipamentos.html",
        {
            "equipamentos": equipamentos
        }
    )


@login_required
def novo_equipamento(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id
    )

    if request.method == "POST":

        tipo = request.POST["tipo"]
        marca = request.POST["marca"]
        modelo = request.POST["modelo"]
        numero_serie = request.POST["numero_serie"]
        acessorios = request.POST["acessorios"]

        garantia = "garantia" in request.POST

        equipamento = Equipamento.objects.create(
            cliente=cliente,
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            acessorios=acessorios,
            garantia=garantia,
        )

        return redirect(
            "nova_ordem",
            equipamento.id
        )

    return render(
        request,
        "equipamentos/novo_equipamento.html",
        {
            "cliente": cliente
        }
    )


@login_required
def editar_equipamento(request, equipamento_id):

    equipamento = get_object_or_404(
        Equipamento,
        id=equipamento_id
    )

    if request.method == "POST":

        equipamento.tipo = request.POST["tipo"]
        equipamento.marca = request.POST["marca"]
        equipamento.modelo = request.POST["modelo"]
        equipamento.numero_serie = request.POST["numero_serie"]
        equipamento.acessorios = request.POST["acessorios"]
        equipamento.garantia = "garantia" in request.POST

        equipamento.save()

        return redirect("lista_equipamentos")

    return render(
        request,
        "equipamentos/editar_equipamento.html",
        {
            "equipamento": equipamento
        }
    )