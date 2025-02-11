from django.utils import timezone
from django.db import models

class Patio(models.Model):
    descricao = models.CharField(max_length=100)
    quantidade_vagas = models.IntegerField()
    vagas_ocupadas = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.descricao
    