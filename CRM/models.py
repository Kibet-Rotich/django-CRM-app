from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('new', 'New'), ('contacted', 'Contacted'), ('qualified', 'Qualified'), ('lost', 'Lost')])
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead: {self.customer.name}"


class Note(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.author.username} on {self.customer.name}"

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('salesman', 'Salesman'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
