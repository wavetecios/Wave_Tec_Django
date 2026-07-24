from django.db import models
from clientes.models import Cliente


class OrdemServico(models.Model):

    STATUS = [
        ("ABERTA", "Aberta"),
        ("EM_ANALISE", "Em análise"),
        ("EM_REPARO", "Em reparo"),
        ("PRONTA", "Pronta"),
        ("ENTREGUE", "Entregue"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    data_abertura = models.DateField(auto_now_add=True)

    defeito = models.TextField()

    reparo = models.TextField(
        blank=True
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    forma_pagamento = models.CharField(
        max_length=20,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="ABERTA"
    )

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"