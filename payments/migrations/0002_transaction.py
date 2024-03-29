# Generated by Django 4.0.3 on 2022-04-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.IntegerField(blank=True, null=True)),
                ('transaction_id', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('paytype', models.CharField(blank=True, max_length=255, null=True)),
                ('order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('liqpay_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.CharField(blank=True, max_length=255, null=True)),
                ('create_date', models.IntegerField(blank=True, null=True)),
                ('end_date', models.IntegerField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('other', models.TextField()),
            ],
        ),
    ]
