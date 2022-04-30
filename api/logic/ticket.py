from user.models import Wallet
from public.models import Lottery, Ticket
import json


def check_solvency(id, price):
    wallet_coins = Wallet.objects.get(user=id).coins
    if int(price) <= wallet_coins:
        return True
    return False


def check_available_tickets(lottery):
    tickets = Ticket.objects.filter(lottery=lottery.id).count()
    if lottery.count_ticket != tickets:
        return True
    return False


def buy_ticket(request):
    lottery = Lottery.objects.get(pk=request.POST['lottery_id'])
    if request.user.is_authenticated:
        if check_solvency(request.user.id, lottery.ticket_price):
            if check_available_tickets(lottery):
                if lottery.status != 'active':
                    return {
                        'message': "Lottery is not active",
                        'type': 'error',
                        'meta': 'not auth'
                    }
                tickets = Ticket.objects.filter(lottery=lottery.id).count()
                wallet = Wallet.objects.get(user=request.user.id)
                wallet.coins -= lottery.ticket_price
                wallet.save()
                ticket = Ticket(
                    user=request.user,
                    lottery=lottery,
                    number=tickets+1
                )
                ticket.save()
                return {
                    'message': "Congratulation!!!",
                    'type': 'success',
                    'meta': 'created',
                    'data': {"ticket_number": ticket.number}
                }
            return {
                'message': "Lottery haven't available tickets.",
                'type': 'error',
                'meta': 'not available'
            }
        return {
            'message': "You don't have enough money to buy.",
            'type': 'error',
            'meta': 'not price'
        }
    return {
        'message': "You must be logged in.",
        'type': 'error',
        'meta': 'not auth'
    }