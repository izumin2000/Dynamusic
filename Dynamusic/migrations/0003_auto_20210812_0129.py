# Generated by Django 3.2.6 on 2021-08-11 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0002_auto_20210809_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sound',
            name='volumes',
        ),
        migrations.AlterField(
            model_name='sound',
            name='notes',
            field=models.CharField(default=',,,,,,,,,,,,,,,', max_length=100),
        ),
    ]
