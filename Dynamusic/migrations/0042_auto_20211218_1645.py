# Generated by Django 3.2.6 on 2021-12-18 07:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0041_auto_20211215_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 18, 16, 45, 10, 250049)),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 18, 16, 45, 10, 248131)),
        ),
    ]
