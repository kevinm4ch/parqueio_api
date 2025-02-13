from datetime import timezone
from typing import List
import random
import string

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router

from .schemas import *
from .models import *

router = Router()


def gerar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )

@router.get("", response=List[TicketOut])
def listar_tickets(request):
    qs = Ticket.objects.all
    return qs

@router.get("/{ticket_cod}", response=TicketOut)
def buscar_ticket(request, ticket_cod:str):
    ticket = get_object_or_404(Ticket, codigo=ticket_cod)
    return ticket

@router.post("")
def novo_ticket(request, payload: TicketIn):
    #Faz o lookup das chaves estrangeiras
    veiculo = get_object_or_404(Veiculo, id=payload.veiculo)
    patio = get_object_or_404(Patio, id=payload.patio)

    if(patio.vagas_ocupadas == patio.quantidade_vagas):
        # Retornando um erro 409 que indica um conflito no estado atual ou seja é preciso que uma vaga seja desocupada
        api = NinjaAPI()
        return api.create_response(request, data={"success": False, "message": "Pátio lotado"},status=409)

    #passa os objetos no lugar dos indices que vem no input
    payload.veiculo = veiculo
    payload.patio = patio
    #cria o objeto com base no input formatado
    ticket = Ticket.objects.create(**payload.dict())

    #gera um codigo e salva o objeto
    ticket.codigo = gerar_codigo()
    ticket.save()

    #Altera a quantidade de vagas no patio
    patio.vagas_ocupadas+=1
    patio.save()


    #Registra no log
    ticketLog = TicketLog.objects.create(ticket= ticket, acao="Gerado com Sucesso!")
    ticketLog.save()

    return {"codigo": ticket.codigo}


@router.put("/pay/{ticket_cod}")
def pagar_ticket(request, ticket_cod:str, payload: TicketPay):
    ticket = get_object_or_404(Ticket, codigo=ticket_cod)

    if(not ticket.ativo):
        api = NinjaAPI()
        return api.create_response(request, data={"Success": False,"message": "Ticket não encontrado"}, status=404)

    # Altera o Ticket
    ticket.valor_pago = payload.valor_pago
    ticket.ativo = False
    ticket.saida = timezone.now()
    ticket.save()

    # Altera a quantidade de vagas occupadas no patio
    patio = get_object_or_404(Patio, id=ticket.patio.id)
    patio.vagas_ocupadas-=1
    patio.save()

    # Registra no log
    ticketLog = TicketLog.objects.create(ticket= ticket, acao="Pago com Sucesso!")
    ticketLog.save()

    return {"Success": True}


