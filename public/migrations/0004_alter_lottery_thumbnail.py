# Generated by Django 4.0.3 on 2022-03-19 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_alter_lottery_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lottery',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='lottery_thumbnail'),
        ),
    ]
