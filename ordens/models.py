from django.db import models
from equipamentos.models import Equipamento


class OrdemServico(models.Model):

    STATUS = [
        ("ABERTA", "Aberta"),
        ("EM_ANALISE", "Em análise"),
        ("AGUARDANDO_PECA", "Aguardando peça"),
        ("EM_REPARO", "Em reparo"),
        ("PRONTO", "Pronto"),
        ("SEM_CONSERTO", "Sem conserto"),
        ("AGUARDANDO_RETIRADA", "Aguardando retirada"),
        ("ENTREGUE", "Entregue"),
    ]

    equipamento_cadastrado = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name="ordens"
    )

    data_abertura = models.DateTimeField(
        auto_now_add=True
    )

    defeito = models.TextField()

    acessorios = models.TextField(
        blank=True
    )

    observacoes = models.TextField(
        blank=True
    )

    reparo = models.TextField(
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
        default="ABERTA"
    )

    @property
    def cliente(self):
        return self.equipamento_cadastrado.cliente

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"