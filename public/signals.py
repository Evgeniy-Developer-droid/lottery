from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from public.models import Lottery, Ticket
from user.models import Wallet


@receiver(post_save, sender=Lottery)
def create_lottery(sender, instance, created, **kwargs):
    if created:
        print('create')


@receiver(post_save, sender=Lottery)
def save_lottery(sender, instance, **kwargs):
    if instance.status == "canceled":
        tickets = Ticket.objects.filter(lottery=instance.pk)
        if instance.type_gift == "money":
            instance.user.wallet.coins += instance.money_gift
            instance.user.wallet.save()
        for ticket in tickets:
            ticket.user.wallet.coins += instance.ticket_price
            ticket.user.wallet.save()
