# Generated by Django 3.2.4 on 2021-11-28 03:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0020_auto_20211123_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sound',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 28, 12, 30, 32, 182111)),
        ),
    ]
