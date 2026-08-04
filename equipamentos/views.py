from django.shortcuts import render, redirect

from clientes.models import Cliente

from .models import Equipamento


def lista_equipamentos(request):

    equipamentos = Equipamento.objects.all()

    return render(
        request,
        "equipamentos/lista_equipamentos.html",
        {
            "equipamentos": equipamentos
        }
    )


def novo_equipamento(request, cliente_id):

    cliente = Cliente.objects.get(id=cliente_id)

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

        print("EQUIPAMENTO SALVO")

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