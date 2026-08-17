from django.contrib import admin

from .models import Lancamento


@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "tipo",
        "descricao",
        "valor",
        "forma_pagamento",
        "data",
    )

    list_filter = (
        "tipo",
        "forma_pagamento",
        "data",
    )

    search_fields = (
        "descricao",
    )