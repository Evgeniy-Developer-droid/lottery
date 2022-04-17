from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from public.forms import SignUpForm, LoginForm
from public.Business.lottery_logic import get_lotterys_for_catalog, get_lottery_by_id, get_tickets_meta, get_winners_single
from user.Business.lottery_logic import get_coins_by_user


def index(request):
    coins = get_coins_by_user(request)
    return render(request, 'public/index.html', {'coins':coins, "title":"Lottery"})


def logout_(request):
    logout(request)
    return redirect('signin')


def signin(request):
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tickets')
                else:
                    return render(request, 'public/login.html', {'form': form, "title": "Login", 'error':"Disabled account", 'coins':coins})
            else:
                return render(request, 'public/login.html', {'form': form, "title": "Login", 'error':"Invalid login", 'coins':coins})
    else:
        form = LoginForm()
    return render(request, 'public/login.html', {'form': form, "title": "Login", 'coins':coins})


def signup(request):
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.type_user = form.cleaned_data.get('type_user')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('tickets')
    else:
        form = SignUpForm()
    return render(request, 'public/signup.html', {'form': form, "title": "Register", 'coins':coins})


def catalog(request):
    coins = get_coins_by_user(request)
    items = get_lotterys_for_catalog()
    paginator = Paginator(items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'public/catalog.html', {'coins':coins, "title": "Catalog", 'page_obj': page_obj})


def single(request, pk):
    coins = get_coins_by_user(request)
    item = get_lottery_by_id(pk)
    if item:
        tickets_meta = get_tickets_meta(pk)
        winners = get_winners_single(pk)
        return render(request, 'public/single.html', {'item': item, "winners": winners, "title": item.name,
                                                      'tickets_meta': tickets_meta, 'coins': coins})
    return render(request, 'public/single.html', {'message': 'Lottery not found', "title": "Ticket", 'coins': coins})