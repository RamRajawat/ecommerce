# Generated by Django 4.0.3 on 2023-10-09 07:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_otpmodel_expiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('accept_order', 'can accept order'), ('reject_order', 'can reject order'), ('view_order', 'can view order'), ('change_order', 'can change order'), ('view_return', 'can view return'), ('accept_return', 'can accept return'), ('reject_return', 'can reject return'), ('change_return', 'can change return'), ('view_dashboard', 'can view dashboard')),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.AlterField(
            model_name='otpmodel',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 9, 7, 12, 31, 292996, tzinfo=utc)),
        ),
    ]
