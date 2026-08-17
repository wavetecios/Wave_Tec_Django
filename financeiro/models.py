from django.db import models

from ordens.models import OrdemServico


class Lancamento(models.Model):

    TIPO_CHOICES = [

        ("RECEITA", "Receita"),
        ("DESPESA", "Despesa"),

    ]

    CATEGORIA_CHOICES = [

        ("SERVICOS", "Serviços"),
        ("PECAS", "Peças"),
        ("ENERGIA", "Energia"),
        ("ALUGUEL", "Aluguel"),
        ("MATERIAL", "Material"),
        ("OUTROS", "Outros"),

    ]

    FORMA_PAGAMENTO = [

        ("DINHEIRO", "Dinheiro"),
        ("PIX", "PIX"),
        ("CARTAO", "Cartão"),
        ("TRANSFERENCIA", "Transferência"),

    ]

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES,
        default="OUTROS"
    )

    descricao = models.CharField(
        max_length=200
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data = models.DateField(
        auto_now_add=True
    )

    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO
    )

    observacoes = models.TextField(
        blank=True
    )

    ordem = models.OneToOneField(
        OrdemServico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lancamento_financeiro"
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-data", "-id"]

        verbose_name = "Lançamento"

        verbose_name_plural = "Financeiro"

    def __str__(self):

        return (
            f"{self.tipo} - "
            f"{self.descricao} - "
            f"R$ {self.valor}"
        )