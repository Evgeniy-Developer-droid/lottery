from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)


class RoomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ur")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="rm", null=True)


class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_message')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="rm_message", null=True)
    read = models.BooleanField(default=False)
    body = models.TextField(default="")
