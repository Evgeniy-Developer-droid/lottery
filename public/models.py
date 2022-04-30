from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import Profile


class Lottery(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('finished', 'Finished'),
    )
    TYPE_GIFT = (('thing', 'Thing'), ('money', 'Money'),)
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    thumbnail = models.ImageField(upload_to='lottery_thumbnail', null=True, blank=True)
    count_ticket = models.IntegerField(default=1)
    count_winners = models.IntegerField(default=1)
    ticket_price = models.FloatField(default=0.0)
    start = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    type_gift = models.CharField(max_length=10, choices=TYPE_GIFT, default='money')
    money_gift = models.FloatField(default=0.0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('playing', 'Playing'),
        ('lose', 'Lose'),
        ('win', 'Win'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='playing')

    def __str__(self):
        return "{} - {} - number - {}".format(self.user.username, self.lottery.name, self.number)


class UserReview(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_author")
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_destination")
    body = models.TextField()


class Report(models.Model):
    name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="")
    text = models.TextField()
