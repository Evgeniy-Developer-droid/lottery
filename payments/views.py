import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from liqpay.liqpay3 import LiqPay

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from user.Business.lottery_logic import get_coins_by_user
from .models import AdminSetting, Transaction


@login_required(login_url='/signin/')
def replenish_the_balance(request):
    coins = get_coins_by_user(request)
    return render(request, "payments/replenish_the_balance.html", {'coins': coins,})


class PayView(TemplateView):
    template_name = 'payments/pay.html'

    def get(self, request, *args, **kwargs):
        credentials = AdminSetting.objects.all().first()
        if credentials and request.GET.get("amount") and request.GET.get("order_id"):
            liqpay = LiqPay(credentials.liqpay_public_key, credentials.liqpay_private_key)
            params = {
                'action': 'pay',
                'amount': request.GET['amount'],
                'currency': 'USD',
                'description': 'Lottery balance',
                'order_id': request.GET['order_id'],
                'version': '3',
                'sandbox': 1, # sandbox mode, set to 1 to enable it
                'server_url': 'https://127.0.0.1:8000/payments/pay-callback/',
                'extra_field': 'some'
            }
            signature = liqpay.cnb_signature(params)
            data = liqpay.cnb_data(params)
            return render(request, self.template_name, {'signature': signature, 'data': data, "title": "pay"})
        return render(request, self.template_name, {'error': "error", "title": "pay"})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):

    def post(self, request, *args, **kwargs):
        credentials = AdminSetting.objects.all().first()
        if credentials:
            liqpay = LiqPay(credentials.liqpay_public_key, credentials.liqpay_private_key)
            data = request.POST.get('data')
            signature = request.POST.get('signature')
            sign = liqpay.str_to_sign(credentials.liqpay_private_key + data + credentials.liqpay_private_key)
            if sign == signature:
                print('callback is valid')
            response = liqpay.decode_data_from_str(data)
            if "status" in response:
                Transaction(
                    payment_id=response.get("payment_id", "null"),
                    transaction_id=response.get("transaction_id", "null"),
                    status=response.get("status", "null"),
                    paytype=response.get("paytype", "null"),
                    user=request.user,
                    order_id=response.get("order_id", "null"),
                    liqpay_order_id=response.get("liqpay_order_id", "null"),
                    currency=response.get("currency", "null"),
                    create_date=response.get("create_date", "null"),
                    end_date=response.get("end_date", "null"),
                    amount=response.get("amount", "null"),
                    other=json.dumps(response)
                ).save()
        return HttpResponse()
