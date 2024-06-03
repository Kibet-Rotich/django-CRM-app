# Generated by Django 5.0.4 on 2024-06-03 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20240601_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('delivery_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='total_price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_mode',
            field=models.CharField(default='Mpesa', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.location'),
        ),
    ]
