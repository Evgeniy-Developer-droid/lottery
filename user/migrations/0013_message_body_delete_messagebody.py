# Generated by Django 4.0.3 on 2022-04-17 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_room_roomuser_message_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='MessageBody',
        ),
    ]