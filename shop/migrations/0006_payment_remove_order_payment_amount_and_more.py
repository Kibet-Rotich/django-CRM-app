# Generated by Django 5.0.4 on 2024-09-13 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order_checkout_request_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkout_request_id', models.CharField(max_length=50, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mpesa_receipt_number', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=15)),
                ('transaction_date', models.CharField(max_length=20)),
                ('result_code', models.IntegerField()),
                ('result_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_phone_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_time',
        ),
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
