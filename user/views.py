from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import logout

from .forms import NewLotteryForm, EmailForm, ResetPasswordForm
from user.Business.lottery_logic import *
from public.Business.lottery_logic import get_tickets_meta, get_reviews_by_user_id, post_review
from user.Business.lottery_logic import get_winners
from .token import account_activation_token


@login_required(login_url='/signin/')
def tickets_view(request):
    if request.user.profile.type_user == "leader":
        return redirect('user-catalog')
    tickets = get_tickets_by_user(request)
    coins = get_coins_by_user(request)
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/tickets.html', {'page_obj':page_obj, "title": "Tickets", 'coins':coins})


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
        "title": "Catalog",
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
                                                             "title": "New lottery",
                                                             'error': result['message'], 'coins':coins})
    else:
        form = NewLotteryForm()
    return render(request, 'user/new-lottery.html', {'form': form, "title": "New lottery", 'coins':coins})


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
                                                          "title": lottery.name,
                                                          "tickets": tickets,
                                                          "lottery": lottery.status in ("finished", "canceled"),
                                                          "wins": winners})
    return render(request, 'user/lottery_view.html', {'coins': coins, 'error': "Lottery not found"})


@login_required(login_url='/signin/')
def settings_(request):
    coins = get_coins_by_user(request)
    return render(request, 'user/settings.html', {'coins': coins, "title": "Settings"})


@login_required(login_url='/signin/')
def user_detail(request, pk):
    coins = get_coins_by_user(request)
    user = get_user_by_id(pk)
    reviews = get_reviews_by_user_id(pk)
    if request.method == "POST":
        result = post_review(request, pk)
        return render(request, 'user/user-detail.html', {'coins': coins,
                                                         'user_data': user,
                                                         "title": user.first_name + user.last_name,
                                                         "result": result,
                                                         "display_rating_button": display_rating_button(request, pk),
                                                         "display_complain_button": display_complain_button(request, pk),
                                                         "reviews": reviews})
    if user:
        return render(request, 'user/user-detail.html', {'coins': coins, "title": user.first_name + user.last_name,
                                                         "display_rating_button": display_rating_button(request, pk),
                                                         "display_complain_button": display_complain_button(request, pk),
                                                         'user_data': user, "reviews": reviews})
    return render(request, 'user/user-detail.html', {'coins': coins, "title": "Not found", 'error': "User doesn`t exist!"})


def password_reset(request):
    coins = get_coins_by_user(request)
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            if settings.EMAIL_CONFIRM:
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'
                try:
                    user = User.objects.get(email=form.cleaned_data.get('email'))
                    message = render_to_string('user/emails/password_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return redirect('password-reset-done')
                except User.DoesNotExist:
                    form = EmailForm()
                    return render(request, 'user/password_reset_form.html',
                                  {'coins': coins, "title": "Change password", 'form': form,
                                   'error': 'User with this email not found!'})
    form = EmailForm()
    return render(request, 'user/password_reset_form.html', {'coins': coins, "title": "Change password", 'form': form})


def password_reset_done(request):
    coins = get_coins_by_user(request)
    return render(request, 'user/password_reset_done.html', {'coins': coins, "title": "Done"})


def password_reset_complete(request):
    coins = get_coins_by_user(request)
    return render(request, 'user/password_reset_complete.html', {'coins': coins, "title": "Done"})


def password_reset_confirm(request, uidb64, token):
    coins = get_coins_by_user(request)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        error = ""
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                pass1 = form.cleaned_data.get('password1', "")
                pass2 = form.cleaned_data.get('password2', "")
                if pass1 == pass2:
                    logout(request)
                    user.set_password(pass1)
                    user.save()
                    return redirect('password-reset-complete')
                else:
                    error = "Password not same"
        form = ResetPasswordForm()
        return render(request, 'user/password_reset_confirm.html', {'coins': coins,
                                                                    'form': form,
                                                                    'error': error,
                                                                    'validlink': True,
                                                                    "title": "Confirm"})
    else:
        return render(request, 'user/password_reset_confirm.html', {'coins': coins, "title": "Confirm"})
