# Generated by Django 3.2.6 on 2021-12-22 05:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0042_auto_20211218_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 22, 14, 41, 49, 56976)),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 22, 14, 41, 49, 56976)),
        ),
    ]
