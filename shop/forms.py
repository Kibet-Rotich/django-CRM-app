# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Location, Item, Order

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'age', 'location', 'password1', 'password2')


class CheckoutForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label="Delivery Location")
    payment_mode = forms.ChoiceField(choices=[('Mpesa', 'Mpesa')], label="Payment Mode")




class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[
                ('pending', 'Pending'),
                ('in progress', 'In Progress'),
                ('completed', 'Completed'),
            ])
        }





class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)



# Form for Item model
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'instock', 'link']

# Form for Location model
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'delivery_price', 'business_days']
