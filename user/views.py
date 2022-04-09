from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewLotteryForm
from user.Business.lottery_logic import *
from public.Business.lottery_logic import get_tickets_meta, get_reviews_by_user_id, post_review
from user.Business.lottery_logic import get_winners


@login_required(login_url='/signin/')
def tickets_view(request):
    if request.user.profile.type_user == "leader":
        return redirect('user-catalog')
    tickets = get_tickets_by_user(request)
    coins = get_coins_by_user(request)
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/tickets.html', {'page_obj':page_obj, 'coins':coins})


@login_required(login_url='/signin/')
def catalog(request):
    if request.user.profile.type_user == "player":
        return redirect('tickets')
    lotterys = get_lotterys_by_user(request)
    coins = get_coins_by_user(request)
    paginator = Paginator(lotterys, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/catalog.html', {
        'page_obj': page_obj,
        'coins': coins
    })


@login_required(login_url='/signin/')
def new_lottery(request):
    if request.user.profile.type_user == "player":
        return redirect('tickets')
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = NewLotteryForm(request.POST)
        result = create_lottery(form, request)
        if result['type'] == 'success':
            return redirect('user-catalog')
        else:
            return render(request, 'user/new-lottery.html', {'form': form,
                                                             'error': result['message'], 'coins':coins})
    else:
        form = NewLotteryForm()
    return render(request, 'user/new-lottery.html', {'form': form, 'coins':coins})


@login_required(login_url='/signin/')
def view_lottery(request, pk):
    if request.user.profile.type_user == "player":
        return redirect('tickets')
    coins = get_coins_by_user(request)
    lottery = get_lottery_by_id(pk, request.user.id)
    if lottery:
        tickets = get_tickets_meta(pk)
        winners = get_winners(lottery.id)
        return render(request, 'user/lottery_view.html', {'coins': coins,
                                                          'item': lottery,
                                                          "tickets": tickets,
                                                          "lottery": lottery.status in ("finished", "canceled"),
                                                          "wins": winners})
    return render(request, 'user/lottery_view.html', {'coins': coins, 'error': "Lottery not found"})


@login_required(login_url='/signin/')
def settings(request):
    coins = get_coins_by_user(request)
    return render(request, 'user/tickets.html', {'coins': coins})


@login_required(login_url='/signin/')
def user_detail(request, pk):
    coins = get_coins_by_user(request)
    user = get_user_by_id(pk)
    reviews = get_reviews_by_user_id(pk)
    if request.method == "POST":
        result = post_review(request, pk)
        return render(request, 'user/user-detail.html', {'coins': coins,
                                                         'user_data': user,
                                                         "result": result,
                                                         "reviews": reviews})
    if user:
        return render(request, 'user/user-detail.html', {'coins': coins, 'user_data': user, "reviews": reviews})
    return render(request, 'user/user-detail.html', {'coins': coins, 'error': "User doesn`t exist!"})
