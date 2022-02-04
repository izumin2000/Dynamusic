# Generated by Django 3.2.9 on 2021-12-15 11:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dynamusic', '0038_auto_20211215_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='icon',
        ),
        migrations.AlterField(
            model_name='chat',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 15, 20, 19, 35, 441849)),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 15, 20, 19, 35, 440950)),
        ),
    ]