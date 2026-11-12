from decimal import Decimal
import csv
import io
import os
import zipfile
from datetime import datetime
from tempfile import NamedTemporaryFile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.text import slugify

from clientes.models import Cliente
from equipamentos.models import Equipamento
from ordens.models import OrdemServico
from financeiro.models import Lancamento


@login_required
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

    ordens_aguardando_retirada = OrdemServico.objects.filter(
        status="AGUARDANDO_RETIRADA"
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


    is_admin = (
        request.user.is_superuser
        or (
            hasattr(request.user, "tecnico")
            and request.user.tecnico is not None
            and request.user.tecnico.perfil == "ADMIN"
        )
    )

    perfil_usuario = "ADMIN" if is_admin else "TECNICO"

    context = {

        "total_clientes": total_clientes,

        "total_equipamentos": total_equipamentos,

        "total_ordens": total_ordens,

        "ordens_abertas": ordens_abertas,

        "ordens_analise": ordens_analise,

        "ordens_reparo": ordens_reparo,

        "ordens_prontas": ordens_prontas,

        "ordens_aguardando_retirada": ordens_aguardando_retirada,

        "ordens_entregues": ordens_entregues,

        "receitas_mes": receitas_mes,

        "despesas_mes": despesas_mes,

        "saldo_mes": saldo_mes,

        "is_admin": is_admin,

        "perfil_usuario": perfil_usuario,

    }


    return render(
        request,
        "core/home.html",
        context
    )


@login_required
def exportar_backup(request):
    if not request.user.is_staff:
        messages.error(request, "Você precisa ter acesso de staff para exportar o backup.")
        return redirect("home")

    formato = request.GET.get("formato", "json").strip().lower()
    hoje = datetime.now().strftime("%Y-%m-%d")

    if formato == "csv":
        with NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            zip_path = temp_zip.name

        try:
            with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as backup_zip:
                for nome_modelo, queryset in [
                    ("clientes.csv", Cliente.objects.all()),
                    ("equipamentos.csv", Equipamento.objects.all()),
                    ("ordens_servico.csv", OrdemServico.objects.all()),
                ]:
                    buffer = io.StringIO()
                    writer = csv.writer(buffer)

                    model = queryset.model
                    fields = [field.name for field in model._meta.fields]
                    writer.writerow(fields)

                    for item in queryset:
                        row = [getattr(item, field) for field in fields]
                        writer.writerow(row)

                    backup_zip.writestr(nome_modelo, buffer.getvalue())

            with open(zip_path, "rb") as arquivo:
                response = HttpResponse(arquivo.read(), content_type="application/zip")
                response["Content-Disposition"] = (
                    f'attachment; filename="backup_wavetec_{hoje}_csv.zip"'
                )
                return response
        finally:
            if os.path.exists(zip_path):
                os.remove(zip_path)

    with NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        arquivo_json = temp_file.name

    try:
        call_command(
            "dumpdata",
            "clientes",
            "equipamentos",
            "ordens",
            "--exclude",
            "contenttypes",
            "--exclude",
            "auth.permission",
            "--indent",
            "2",
            "--output",
            arquivo_json,
        )

        with open(arquivo_json, "rb") as arquivo:
            response = HttpResponse(arquivo.read(), content_type="application/json")
            response["Content-Disposition"] = (
                f'attachment; filename="backup_wavetec_{hoje}.json"'
            )
            return response
    finally:
        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)