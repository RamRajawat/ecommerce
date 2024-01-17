# Generated by Django 4.0.3 on 2023-10-21 09:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_otpmodel_expiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinorderplaced',
            name='discounted_price',
        ),
        migrations.AddField(
            model_name='productinorderplaced',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 21, 9, 56, 9, 44417, tzinfo=utc)),
        ),
    ]
