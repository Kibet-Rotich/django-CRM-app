# Generated by Django 5.0.4 on 2024-09-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_payment_remove_order_payment_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('failed', 'Failed'), ('successful', 'Successful')], default='pending', max_length=20),
        ),
    ]
