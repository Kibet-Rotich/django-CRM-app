# Generated by Django 5.0.4 on 2024-09-12 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_cartitem_cart_remove_cartitem_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_request_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]