# Generated by Django 3.2.9 on 2021-12-15 11:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0039_auto_20211215_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='account',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='chat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 15, 20, 25, 46, 247488)),
        ),
        migrations.AlterField(
            model_name='information',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 15, 20, 25, 46, 246595)),
        ),
    ]
