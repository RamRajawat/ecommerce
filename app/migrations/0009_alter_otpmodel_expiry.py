# Generated by Django 4.0.3 on 2023-10-13 09:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_otpmodel_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 13, 9, 24, 6, 697133, tzinfo=utc)),
        ),
    ]
