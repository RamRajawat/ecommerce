# Generated by Django 4.0.3 on 2023-11-04 21:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_orderplaced_status_alter_otpmodel_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel'), ('Pending', 'Pending')], default='Pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 21, 49, 5, 493026, tzinfo=utc)),
        ),
    ]
