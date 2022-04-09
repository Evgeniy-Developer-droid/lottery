from django.urls import path
from . import views

urlpatterns = [
    path('buy-ticket', views.buy_ticket_view),
]