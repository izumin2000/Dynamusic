# Generated by Django 3.2.6 on 2021-09-13 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0013_auto_20210914_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sound',
            name='track13',
            field=models.CharField(default='-', max_length=13),
        ),
    ]
