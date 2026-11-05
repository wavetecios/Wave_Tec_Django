from django.db import models

from ordens.models import OrdemServico


class Atendimento(models.Model):

    STATUS = [
        ("EM_ANALISE", "Em análise"),
        ("AGUARDANDO_PECA", "Aguardando peça"),
        ("EM_REPARO", "Em reparo"),
        ("PRONTO", "Pronto"),
        ("SEM_CONSERTO", "Sem conserto"),
        ("AGUARDANDO_RETIRADA", "Aguardando retirada"),
        ("ENTREGUE", "Entregue"),
    ]

    ordem = models.OneToOneField(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name="atendimento"
    )

    diagnostico = models.TextField(
        blank=True
    )

    servico_executado = models.TextField(
        blank=True
    )

    pecas_utilizadas = models.TextField(
        blank=True
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    forma_pagamento = models.CharField(
        max_length=30,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="EM_ANALISE"
    )

    data_inicio = models.DateTimeField(
        auto_now_add=True
    )

    data_finalizacao = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Atendimento OS {self.ordem.id}"