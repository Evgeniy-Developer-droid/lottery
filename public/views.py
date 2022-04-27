from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from public.forms import SignUpForm, LoginForm, ContactUsForm
from public.Business.lottery_logic import get_lotterys_for_catalog, get_lottery_by_id, get_tickets_meta, get_winners_single
from public.models import Report
from user.Business.lottery_logic import get_coins_by_user
from user.token import account_activation_token


def index(request):
    coins = get_coins_by_user(request)
    return render(request, 'public/index.html', {'coins': coins, "title": "Lottery"})


def privacy(request):
    coins = get_coins_by_user(request)
    return render(request, 'public/privacy.html', {'coins': coins, "title": "Privacy and policy"})


def logout_(request):
    logout(request)
    return redirect('signin')


def contact_us(request):
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            email = form.cleaned_data.get('email', '')
            text = form.cleaned_data.get('text', '')
            Report(name=name, email=email, text=text).save()
            return render(request, 'public/contact_us.html', {'coins': coins, "saved": True, "title": "Contact us"})
    form = ContactUsForm()
    return render(request, 'public/contact_us.html', {'coins': coins, 'form': form, "title": "Contact us"})


def signin(request):
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            print("error", form.errors)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tickets')
                else:
                    return render(request, 'public/login.html', {'form': form, "title": "Login",
                                                                 'error': "Disabled account", 'coins': coins})
            else:
                return render(request, 'public/login.html', {'form': form, "title": "Login",
                                                             'error': "Invalid login or password", 'coins': coins})
    else:
        form = LoginForm()
    return render(request, 'public/login.html', {'form': form, "title": "Login", 'coins': coins})


def signup(request):
    coins = get_coins_by_user(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.type_user = form.cleaned_data.get('type_user')

            if settings.EMAIL_CONFIRM:
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'
                message = render_to_string('user/emails/acc_active_email.html', {
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
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                user.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect('tickets')
    else:
        form = SignUpForm()
    return render(request, 'public/signup.html', {'form': form, "title": "Register", 'coins': coins})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


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