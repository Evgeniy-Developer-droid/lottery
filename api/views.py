from django.shortcuts import render
from django.http import JsonResponse
from .logic import ticket


def buy_ticket_view(request):
    invoice = ticket.buy_ticket(request)
    return JsonResponse(invoice)
