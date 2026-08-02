from django.shortcuts import render, redirect
from clientes.models import Cliente
from .models import Equipamento


def novo_equipamento(request):

    if request.method == "POST":

        cliente_id = request.POST["cliente"]
        tipo = request.POST["tipo"]
        marca = request.POST["marca"]
        modelo = request.POST["modelo"]
        numero_serie = request.POST["numero_serie"]
        acessorios = request.POST["acessorios"]

        garantia = "garantia" in request.POST

        print(cliente_id)
        print(tipo)
        print(marca)
        print(modelo)
        print(numero_serie)
        print(acessorios)
        print(garantia)

        
        cliente = Cliente.objects.get(id=cliente_id)

        Equipamento.objects.create(
            cliente=cliente,
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            numero_serie=numero_serie,
            acessorios=acessorios,
            garantia=garantia,
        )

        print("EQUIPAMENTO SALVO")

def lista_equipamentos(request):

    equipamentos = Equipamento.objects.all()

    return render(
        request,
        "equipamentos/lista_equipamentos.html",
        {
            "equipamentos": equipamentos
        }
    )    

    # ESTA LINHA TEM QUE FICAR FORA DO IF
    clientes = Cliente.objects.all()

    return render(
        request,
        "equipamentos/novo_equipamento.html",
        {
            "clientes": clientes
        }
    )