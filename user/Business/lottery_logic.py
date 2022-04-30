import random

from django.contrib.auth.models import User

from public.models import Lottery, Ticket
from user.models import Wallet, Rating, Complain


def create_lottery(form, request):
    if form.is_valid() and ('thumbnail' in request.FILES):
        tickets = int(request.POST.get('count_ticket'))
        winners = int(request.POST.get('count_winners'))
        if winners > tickets:
            return {'message': 'The number of winners is greater than the number of tickets', 'type': 'error'}
        if request.POST.get('type_gift') == 'money':
            main_sum = float(request.POST.get('money_gift')) * winners
            if request.user.wallet.coins > main_sum:
                wallet = Wallet.objects.get(user=request.user.pk)
                wallet.coins -= main_sum
                wallet.save()
            else:
                return {'message': 'You don`t have enough money', 'type': 'error'}
        lottery = form.save()
        lottery.refresh_from_db()
        lottery.user = request.user
        lottery.thumbnail = request.FILES['thumbnail']
        lottery.save()
        return {'message': 'SUCCESS', 'type': 'success'}
    else:
        return {'message': 'Thumbnail is required!', 'type': 'error'}


def get_lotterys_by_user(request):
    return Lottery.objects.filter(user=request.user.pk)


def get_tickets_by_user(request):
    return Ticket.objects.filter(user=request.user.id)


def get_coins_by_user(request):
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(user=request.user.pk)
        return wallet.coins
    return 0


def get_lottery_by_id(pk, user_id):
    try:
        return Lottery.objects.get(pk=pk, user=user_id)
    except Lottery.DoesNotExist:
        return False


def get_winners(lottery_id):
    result = list()
    for winner in Ticket.objects.filter(lottery=lottery_id, status="win"):
        result.append({
                'full_name': winner.user.first_name+" "+winner.user.last_name,
                'number': winner.number,
                'user_id': winner.user.id
            })
    return result


def define_lottery_winners(request, data):

    def get_winners_data(wins):
        info = list()
        for winner in wins:
            info.append({
                'full_name': winner.user.first_name+" "+winner.user.last_name,
                'number': winner.number,
                'user_id': winner.user.id
            })
        return info

    def validation_error(lot, req):
        if lot.user.id != req.user.id:
            return {"message": "You don`t have permission for this lottery.", 'type': "error"}
        if lot.status == 'canceled':
            return {"message": "Lottery canceled.", 'type': "error"}
        if lot.status == 'finished':
            return {"message": "Lottery finished.", 'type': "error"}
        return False

    try:
        lottery = Lottery.objects.get(pk=data['id'])
        valid_error = validation_error(lottery, request)
        if not valid_error:
            challengers = Ticket.objects.filter(lottery=lottery.id)
            owner_wallet = Wallet.objects.get(user=request.user.id)
            count_winners = lottery.count_winners
            if challengers.count() == 0:

                if lottery.type_gift == 'money':
                    owner_wallet.coins += lottery.money_gift
                    owner_wallet.save()

                lottery.status = 'finished'
                lottery.save()
                return {'message': "Lottery is finish, winners not found because count of players 0. Your money is back",
                        'type': 'success'}
            if count_winners >= challengers.count():
                winners = challengers
            else:
                possible_ids = list(challengers.values_list('id', flat=True))
                possible_ids = random.choices(possible_ids, k=count_winners)
                winners = challengers.filter(pk__in=possible_ids)  # get winners
                lossers = challengers.exclude(pk__in=possible_ids)  # get lossers
                lossers.update(status='lose')

            # add balance to owner
            owner_wallet.coins += challengers.count() * lottery.ticket_price
            owner_wallet.save()

            if lottery.type_gift == 'money':
                for winner in winners:
                    # add gift balance
                    wallet_winner = Wallet.objects.get(user=winner.user.pk)
                    wallet_winner.coins += lottery.money_gift
                    wallet_winner.save()

            winners.update(status='win')
            info_winners = get_winners_data(winners)
            lottery.status = 'finished'
            lottery.save()
            return {'message': "Success!", 'type': 'success', 'data': info_winners}
        else:
            return valid_error
    except Lottery.DoesNotExist:
        return {'message': "Lottery doesn`t exist.", 'type': 'error'}


def get_user_by_id(id):
    try:
        return User.objects.get(pk=id)
    except User.DoesNotExist:
        return False


def permission_estimate(current_user, target_user):
    rating = Rating.objects.filter(user=target_user.pk, ratinger=current_user.pk)
    if rating.exists() or (current_user.profile.type_user == "leader" and target_user.profile.type_user == "leader") or current_user.pk == target_user.pk:
        return False
    return True


def permission_complain(current_user, target_user):
    complain = Complain.objects.filter(user=target_user.pk, complainer=current_user.pk)
    print(current_user.profile.type_user == "leader" and target_user.profile.type_user == "leader")
    if complain.exists() or (current_user.profile.type_user == "leader" and target_user.profile.type_user == "leader") or current_user.pk == target_user.pk:
        return False
    return True


def display_rating_button(request, target_id):
    rating = Rating.objects.filter(user=target_id, ratinger=request.user.pk)
    if rating.exists() or (request.user.profile.type_user == "leader" and User.objects.get(pk=target_id).profile.type_user == "leader") or request.user.pk == target_id:
        return False
    return True


def display_complain_button(request, target_id):
    complain = Complain.objects.filter(user=target_id, complainer=request.user.pk)
    if complain.exists() or (request.user.profile.type_user == "leader" and User.objects.get(pk=target_id).profile.type_user == "leader") or request.user.pk == target_id:
        return False
    return True
