from datetime import datetime
from ninja import Schema

from patio.models import Patio
from patio.schemas import PatioOut
from .models import Ticket, Veiculo

class TicketIn(Schema):
    patio: int = any
    veiculo: int = any

class VeiculoOut(Schema):
    id: int
    descricao: str

class TicketOut(Schema):
    id: int
    codigo: str
    veiculo: VeiculoOut
    patio: PatioOut
    entrada: datetime
    saida: datetime | None
    valor_pago: float | None
    ativo: bool

class TicketPay(Schema):
    valor_pago: float
