# Generated by Django 4.0.3 on 2022-04-29 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_lottery_money_gift_lottery_type_gift_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottery',
            name='count_winners',
            field=models.IntegerField(default=1),
        ),
    ]
