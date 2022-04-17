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
    rating = models.FloatField(default=0.0)
    rating_sum = models.FloatField(default=0.0)
    complaints = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Complain(models.Model):
    complainer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='complainer_comp', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comp')


class Rating(models.Model):
    ratinger = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='ratinger_rating', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rating')
    value = models.IntegerField(default=0)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_message')
    read = models.BooleanField(default=False)


class MessageBody(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    body = models.TextField()


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=Complain)
def rating(sender, instance, created, **kwargs):
    if created:
        criminal = Profile.objects.get(user=instance.user.pk)
        criminal.complaints += 1
        criminal.save()


@receiver(post_save, sender=Rating)
def rating(sender, instance, created, **kwargs):
    if created:
        target_profile = Profile.objects.get(user=instance.user.pk)
        all_rat = Rating.objects.filter(user=instance.user.pk).count()
        result = (target_profile.rating_sum + float(instance.value)) / all_rat
        target_profile.rating_sum += float(instance.value)
        target_profile.rating = result
        target_profile.save()