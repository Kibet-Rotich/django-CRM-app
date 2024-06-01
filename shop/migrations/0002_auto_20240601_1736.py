from django.db import migrations
from faker import Faker
from shop.models import Item

def generate_sample_data(apps, schema_editor):
    fake = Faker()
    for _ in range(10):  # Generate 10 sample items
        name = fake.name()  # Generate a fake name
        description = fake.text()  # Generate a fake description
        price = fake.random_number(digits=2)  # Generate a random price
        instock = fake.random_number(digits=3)  # Generate a random quantity in stock
        Item.objects.create(name=name, description=description, price=price, instock=instock)

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),  # Add dependencies of your previous migrations
    ]

    operations = [
        migrations.RunPython(generate_sample_data),
    ]
