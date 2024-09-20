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


from django import forms
from .models import Order

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



from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
