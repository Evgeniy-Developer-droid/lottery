from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from user.Business.lottery_logic import get_coins_by_user


@login_required(login_url='/signin/')
def messages(request):
    coins = get_coins_by_user(request)
    return render(request, "messages_app/messages.html", {'coins': coins})
