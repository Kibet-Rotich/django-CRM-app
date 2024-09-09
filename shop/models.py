# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=20)
    location = models.CharField(max_length=100)


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instock = models.DecimalField(max_digits=7, decimal_places = 0)
    # Additional fields as needed

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20)  # e.g., 'pending', 'completed', 'failed'
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_phone_number = models.CharField(max_length=15, blank=True, null=True)
    payment_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate the total price based on the quantity and product price
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


