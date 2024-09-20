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
    business_days = models.PositiveIntegerField(default=1)  # New field for processing time

    def __str__(self):
        return self.name


    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('successful', 'Successful')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # For production status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')  # New field for payment status
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    checkout_request_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"



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






class Payment(models.Model):
    checkout_request_id = models.CharField(max_length=50, unique=True)  # Unique ID from the Daraja callback
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.CharField(max_length=20)
    result_code = models.IntegerField()
    result_description = models.CharField(max_length=255)

    def __str__(self):
        return f"Payment {self.mpesa_receipt_number} for {self.checkout_request_id}"