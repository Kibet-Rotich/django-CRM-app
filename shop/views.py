from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm
def index(request):
    return render(request, 'index.html')

from .models import Item

def home(request):
    # Retrieve all items from the database
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})




def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, CartItem



@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Use defaults to set initial quantity if creating a new CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item, defaults={'quantity': 1})
    if not created:
        # Increment the quantity if the CartItem already exists
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('home')  # Redirect to cart detail page




from django.db.models import Sum
@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = cart_items.aggregate(Sum('item__price'))['item__price__sum']
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total_amount': total_amount})




def update_cart_item_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart_detail')




from .models import CartItem, Order, Location
from .forms import CheckoutForm

def checkout(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_price = sum(item.quantity * item.item.price for item in cart_items)
    delivery_price = 0

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            payment_mode = form.cleaned_data['payment_mode']
            delivery_price = location.delivery_price
            total_amount = total_price + delivery_price
            
            # Create the order
            order = Order.objects.create(
                user=request.user,
                location=location,
                total_price=total_amount,
                payment_mode=payment_mode
            )
            
            # Clear the cart (optional)
            cart_items.delete()
            
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'delivery_price': delivery_price
    })

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
