# Generated by Django 3.2.9 on 2022-01-13 15:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0060_auto_20220113_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 0, 35, 2, 183590)),
        ),
    ]