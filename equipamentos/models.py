from django.db import models
from clientes.models import Cliente


class Equipamento(models.Model):

    TIPOS = [
        ("TV", "Televisão"),
        ("NOTE", "Notebook"),
        ("PC", "Computador"),
        ("CEL", "Celular"),
        ("SOM", "Som"),
        ("MICRO", "Micro-ondas"),
        ("OUTRO", "Outro"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    marca = models.CharField(
        max_length=50
    )

    modelo = models.CharField(
        max_length=50
    )

    numero_serie = models.CharField(
        max_length=100,
        blank=True
    )

    acessorios = models.TextField(
        blank=True
    )

    garantia = models.BooleanField(
        default=False
    )

    data_entrada = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        default="Em análise"
    )

    def __str__(self):
        return f"{self.cliente.nome} - {self.marca} {self.modelo}"