# Generated by Django 4.0 on 2022-01-08 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0055_alter_chat_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 9, 1, 31, 59, 543687)),
        ),
    ]