# Register your models here.
from django.contrib import admin
from .models import Cart, CartItem,Location,Order,Item

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Item)