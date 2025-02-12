from django.utils import timezone
from django.db import models
from patio.models import Patio

class Veiculo(models.Model):
    descricao = models.CharField(max_length=20)

class Ticket(models.Model):
    codigo = models.CharField(max_length=10)
    patio = models.ForeignKey(Patio, on_delete=models.CASCADE)   
    entrada = models.DateTimeField(default=timezone.now)
    saida = models.DateTimeField(null=True, blank=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.RESTRICT)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ativo = models.BooleanField(default=True)

class TicketLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.RESTRICT)
    acao = models.CharField(max_length=20)
    data_hora = models.DateTimeField(default=timezone.now)