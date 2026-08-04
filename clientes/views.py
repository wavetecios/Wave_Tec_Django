from django.shortcuts import render, redirect

from .models import Cliente


def lista_clientes(request):

    clientes = Cliente.objects.all()

    return render(
        request,
        "clientes/lista_clientes.html",
        {
            "clientes": clientes
        }
    )


def novo_cliente(request):

    if request.method == "POST":

        nome = request.POST["nome"]
        telefone = request.POST["telefone"]
        endereco = request.POST["endereco"]

        cliente = Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            endereco=endereco
        )

        print("CLIENTE SALVO")

        return redirect(
            "novo_equipamento",
            cliente.id
        )

    return render(
        request,
        "clientes/novo_cliente.html"
    )