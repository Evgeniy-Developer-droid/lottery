# Generated by Django 4.0.3 on 2022-04-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profile_complaints_profile_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='count_rating',
            field=models.IntegerField(default=0),
        ),
    ]
