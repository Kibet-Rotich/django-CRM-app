# Register your models here.
from django.contrib import admin
from .models import Location,Order,Item


admin.site.register(Location)
admin.site.register(Order)
admin.site.register(Item)