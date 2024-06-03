# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Location

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'name', 'age', 'location', 'password1', 'password2')


class CheckoutForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), label="Delivery Location")
    payment_mode = forms.ChoiceField(choices=[('Mpesa', 'Mpesa')], label="Payment Mode")

