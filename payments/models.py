from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import Wallet


class AdminSetting(models.Model):
    liqpay_public_key = models.CharField(max_length=255, null=True, blank=True)
    liqpay_private_key = models.CharField(max_length=255, null=True, blank=True)


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    payment_id = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    paytype = models.CharField(max_length=255, null=True, blank=True)
    order_id = models.CharField(max_length=255, null=True, blank=True)
    liqpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.IntegerField(null=True, blank=True)
    end_date = models.IntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sended_to_user = models.BooleanField(default=False)
    other = models.TextField()


@receiver(post_save, sender=Transaction)
def update_transaction(sender, instance, created, **kwargs):
    if created:
        if instance.status in ("sandbox", "success") and not instance.sended_to_user:
            wallet = Wallet.objects.get(user=instance.user.pk)
            wallet.coins += int(instance.amount)
            wallet.save()
        instance.sended_to_user = True
        instance.save()


