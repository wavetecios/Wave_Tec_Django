from django.shortcuts import render, redirect
from .models import OrdemServico
from clientes.models import Cliente


def lista_ordens(request):

    ordens = OrdemServico.objects.all()

    return render(
        request,
        "ordens/lista_ordens.html",
        {
            "ordens": ordens
        }
    )


def nova_ordem(request):

    if request.method == "POST":

        print("ENTROU NO POST")

        cliente_id = request.POST["cliente"]
        equipamento = request.POST["equipamento"]
        marca = request.POST["marca"]
        modelo = request.POST["modelo"]
        acessorios= request.POST["acessorios"]
        defeito = request.POST["defeito"]
        observacoes = request.POST["observacoes"]

        print("Observações recebidas:", repr(observacoes))

        cliente = Cliente.objects.get(id=cliente_id)

        OrdemServico.objects.create(
            cliente=cliente,
            equipamento=equipamento,
            marca = marca,
            modelo=modelo,
            acessorios=acessorios,
            defeito=defeito,
            observacoes=observacoes
           
        )

        print("CHEGOU AQUI - ORDEM SALVA")

        return redirect("lista_ordens")

    clientes = Cliente.objects.all()

    return render(
        request,
        "ordens/nova_ordem.html",
        {
            "clientes": clientes
        }
    )