# Generated by Django 4.0.3 on 2022-04-17 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_message_messagebody'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagebody',
            name='message',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='MessageBody',
        ),
    ]
