from datetime import datetime
from ninja import Schema

from patio.schemas import PatioOut
from .models import Ticket

class TicketIn(Schema):
    codigo: str
    patio: int
    veiculo: int
    saida: datetime = None
    valor_pago: float = None

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
