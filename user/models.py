from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    USER_CHOICES = (
        ('leader', 'LEADER'),
        ('player', 'PLAYER'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_user = models.CharField(max_length=6, choices=USER_CHOICES, default='player')
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="avatars", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance)
    instance.profile.save()
