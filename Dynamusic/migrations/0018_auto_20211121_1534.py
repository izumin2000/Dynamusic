# Generated by Django 3.2.9 on 2021-11-21 06:34

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dynamusic', '0017_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Midi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attach', models.FileField(blank=True, null=True, upload_to='midi/', validators=[django.core.validators.FileExtensionValidator(['mid'])], verbose_name='midiファイル')),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='account_image',
        ),
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sound',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 21, 15, 34, 31, 669097)),
        ),
        migrations.AddField(
            model_name='sound',
            name='place',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track1',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track2',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track3',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track4',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track5',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track6',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track7',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track8',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='sound',
            name='track9',
            field=models.CharField(default='', max_length=15),
        ),
    ]
