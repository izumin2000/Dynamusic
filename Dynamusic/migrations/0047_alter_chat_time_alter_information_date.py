# Generated by Django 4.0 on 2021-12-21 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0046_alter_chat_time_alter_information_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 21, 22, 45, 17, 106054)),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 21, 22, 45, 17, 96154)),
        ),
    ]
