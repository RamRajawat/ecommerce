# Generated by Django 4.0.3 on 2023-10-08 14:54

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_review_rate_review_ip_review_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='otp should be in six digits', regex='^\\d{6}$')])),
                ('phone', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message='phone number should exactly be in 10 digits', regex='^\\d{10}$')])),
                ('expiry', models.DateTimeField(default=datetime.datetime(2023, 10, 8, 14, 59, 16, 770115, tzinfo=utc))),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='datetime_of_payment',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'SUCCESS'), (2, 'FAILURE'), (3, 'PENDING')], default=3),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='total_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='pending', max_length=15),
        ),
        migrations.CreateModel(
            name='ProductInOrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('discounted_price', models.FloatField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.orderplaced')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
            options={
                'unique_together': {('order', 'product')},
            },
        ),
    ]