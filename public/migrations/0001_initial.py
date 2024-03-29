# Generated by Django 4.0.3 on 2022-03-18 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='lottery_thumbnail')),
                ('count_ticket', models.IntegerField(default=1)),
                ('ticket_price', models.IntegerField(default=1)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('finish', models.DateTimeField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('canceled', 'Canceled'), ('finished', 'Finished')], default='active', max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
