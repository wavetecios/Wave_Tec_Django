from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cliente


@login_required
def lista_clientes(request):

    clientes = Cliente.objects.all()

    return render(
        request,
        "clientes/lista_clientes.html",
        {
            "clientes": clientes
        }
    )


@login_required
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

        return redirect(
            "novo_equipamento",
            cliente.id
        )

    return render(
        request,
        "clientes/novo_cliente.html"
    )


@login_required
def editar_cliente(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id
    )

    if request.method == "POST":

        cliente.nome = request.POST["nome"]
        cliente.telefone = request.POST["telefone"]
        cliente.endereco = request.POST["endereco"]

        cliente.save()

        return redirect("lista_clientes")

    return render(
        request,
        "clientes/editar_cliente.html",
        {
            "cliente": cliente
        }
    )