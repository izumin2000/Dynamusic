# Generated by Django 3.2.6 on 2021-08-11 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0004_auto_20210812_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='sound',
            name='place',
            field=models.CharField(default='', max_length=8),
        ),
    ]
