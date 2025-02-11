from datetime import timezone
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from .schemas import *
from .models import *

router = Router()

@router.get("", response=List[TicketOut])
def listar_tickets(request):
    qs = Ticket.objects.all
    return qs

@router.get("/{ticket_id}", response=TicketOut)
def buscar_ticket(request, ticket_id:int):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return ticket

@router.post("")
def novo_ticket(request, payload: TicketIn):
    payload.veiculo = get_object_or_404(Veiculo, id=payload.veiculo)
    payload.patio = get_object_or_404(Patio, id=payload.patio)

    ticket = Ticket.objects.create(**payload.dict())
    ticket.save()

    ticketLog = TicketLog.objects.create(ticket= ticket, acao="Gerado com Sucesso!")
    ticketLog.save()

    return {"id": ticket.id}

@router.put("/pay/{ticket_id}")
def pagar_ticket(request, ticket_id:int, payload: TicketPay):
    ticket = get_object_or_404(Ticket, id=ticket_id)


    if(not ticket.ativo):
        return {"success": False, "message": "Ticket não encontrado"}


    setattr(ticket, "valor_pago", payload.valor_pago)
    setattr(ticket, "ativo", False)
    setattr(ticket, "saida", timezone.now())
    ticket.save()

    ticketLog = TicketLog.objects.create(ticket= ticket, acao="Pago com Sucesso!")
    ticketLog.save()

    return {"Success": True}


