
from ninja import Schema


class PatioIn(Schema):
    descricao: str
    quantidade_vagas: int

class PatioOut(Schema):
    id: int
    descricao: str
    quantidade_vagas: int
    vagas_ocupadas: int
    