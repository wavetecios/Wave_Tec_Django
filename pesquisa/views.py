from django.shortcuts import render

from django.db.models import Q

from clientes.models import Cliente
from equipamentos.models import Equipamento
from ordens.models import OrdemServico


def pesquisa_global(request):

    termo = request.GET.get("q", "").strip()

    clientes = []
    equipamentos = []
    ordens = []

    if termo:

        clientes = Cliente.objects.filter(

            Q(nome__icontains=termo) |
            Q(telefone__icontains=termo) |
            Q(endereco__icontains=termo)

        ).order_by("nome")

        equipamentos = Equipamento.objects.filter(

            Q(marca__icontains=termo) |
            Q(modelo__icontains=termo) |
            Q(numero_serie__icontains=termo) |
            Q(tipo__icontains=termo) |
            Q(cliente__nome__icontains=termo)

        ).order_by("cliente__nome")

        
        ordens = OrdemServico.objects.filter(

            Q(defeito__icontains=termo) |
            Q(observacoes__icontains=termo) |
            Q(equipamento_cadastrado__cliente__nome__icontains=termo) |
            Q(equipamento_cadastrado__cliente__telefone__icontains=termo) |
            Q(equipamento_cadastrado__marca__icontains=termo) |
            Q(equipamento_cadastrado__modelo__icontains=termo) |
            Q(equipamento_cadastrado__numero_serie__icontains=termo)

        ).order_by("-id")
        

    
    return render(

        request,

        "pesquisa/pesquisa.html",

        {

            "termo": termo,

            "clientes": clientes,
            "equipamentos": equipamentos,
            "ordens": ordens,

        }

    )