from datetime import datetime
from ninja import Schema

from patio.schemas import PatioOut

class TicketIn(Schema):
    patio: int
    veiculo: int

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
