# Generated by Django 4.0.3 on 2022-04-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottery',
            name='money_gift',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='lottery',
            name='type_gift',
            field=models.CharField(choices=[('thing', 'Thing'), ('money', 'Money')], default='money', max_length=10),
        ),
        migrations.AlterField(
            model_name='lottery',
            name='ticket_price',
            field=models.FloatField(default=0.0),
        ),
    ]