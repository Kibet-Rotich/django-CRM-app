# Register your models here.
from django.contrib import admin
from .models import Location,Order,Item,Payment,OrderItem


admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Payment)
admin.site.register(OrderItem)