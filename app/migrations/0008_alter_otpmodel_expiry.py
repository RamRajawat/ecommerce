# Generated by Django 4.0.3 on 2023-10-12 04:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_otpmodel_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 12, 4, 16, 19, 959316, tzinfo=utc)),
        ),
    ]
