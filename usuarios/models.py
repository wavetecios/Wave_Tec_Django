from django.conf import settings
from django.db import models


class Tecnico(models.Model):
    PERFIS = [
        ('ADMIN', 'Administrador'),
        ('TECNICO', 'Técnico'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tecnico',
        null=True,
        blank=True,
    )

    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    perfil = models.CharField(max_length=20, choices=PERFIS, default='TECNICO')
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Técnico'
        verbose_name_plural = 'Técnicos'

    def __str__(self):
        return self.nome
