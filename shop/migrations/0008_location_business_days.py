# Generated by Django 5.0.4 on 2024-09-20 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='business_days',
            field=models.PositiveIntegerField(default=1),
        ),
    ]