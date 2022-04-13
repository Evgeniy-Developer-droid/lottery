from django.urls import path

from payments.views import PayView, PayCallbackView, replenish_the_balance


urlpatterns = [
    path('pay/', PayView.as_view(), name='pay_view'),
    path('pay-callback/', PayCallbackView.as_view(), name='pay_callback'),
    path('replenish-the-balance/', replenish_the_balance, name="replenish_the_balance")
]