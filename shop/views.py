from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm

from .models import Item

def index(request):
    # Retrieve all items from the database
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

from django.shortcuts import render
from .models import Location

def cart(request):
    # Fetch all available locations for the checkout form
    locations = Location.objects.all()
    
    # Render the combined cart and checkout template
    return render(request, 'cart_detail.html', {'locations': locations})




#payment
import base64
import base64
import requests
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Location

def get_access_token():
    consumer_key = settings.DARAJA_CONSUMER_KEY
    consumer_secret = settings.DARAJA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_url, auth=(consumer_key, consumer_secret))
    json_response = r.json()
    return json_response['access_token']


import json
import requests
import base64
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Order, OrderItem, Location

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = float(request.POST.get('amount', 0))
        location_id = request.POST.get('location_id')
        cart_items = json.loads(request.POST.get('cart_items', '[]'))

        if not phone_number or not amount or not location_id or not cart_items:
            return JsonResponse({'error': 'Phone number, amount, location, and cart items are required'}, status=400)

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return JsonResponse({'error': 'Invalid location ID'}, status=400)

        # Create a new order
        order = Order.objects.create(
            amount=amount,
            phone_number=phone_number,
            status='pending',
            location=location
        )

        # Save order items
        for item in cart_items:
            product = Item.objects.get(id=item['id'])  # Retrieve the Item object using the product ID
            OrderItem.objects.create(
            order=order,
            product=product,  # Assign the product object
            quantity=item['quantity']
    )


        # Continue with the payment process (STK Push)
        access_token = get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_short_code = settings.DARAJA_SHORTCODE
        lipa_na_mpesa_online_passkey = settings.DARAJA_PASSKEY
        data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
        encoded_string = base64.b64encode(data_to_encode.encode())
        password = encoded_string.decode('utf-8')

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.DARAJA_CALLBACK_URL,
            "AccountReference": str(order.id),
            "TransactionDesc": "Payment for order"
        }

        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get('ResponseCode') == '0':
            order.checkout_request_id = response_data.get('CheckoutRequestID')
            order.save()
            return JsonResponse({'message': 'Payment initiated successfully', 'order_id': order.id}, status=200)
        else:
            return JsonResponse({'error': 'Failed to initiate payment', 'details': response_data}, status=400)

    return HttpResponse(status=405)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Order

@csrf_exempt
def payment_confirmation(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            payment_data = json.loads(request.body)

            # Extract callback data
            stk_callback = payment_data['Body']['stkCallback']
            result_code = stk_callback['ResultCode']
            checkout_request_id = stk_callback['CheckoutRequestID']
            result_description = stk_callback['ResultDesc']

            # Extract payment details
            callback_metadata = stk_callback['CallbackMetadata']['Item']
            amount = None
            mpesa_receipt_number = None
            transaction_date = None
            phone_number = None

            for item in callback_metadata:
                if item['Name'] == 'Amount':
                    amount = item['Value']
                if item['Name'] == 'MpesaReceiptNumber':
                    mpesa_receipt_number = item['Value']
                if item['Name'] == 'TransactionDate':
                    transaction_date = item['Value']
                if item['Name'] == 'PhoneNumber':
                    phone_number = item['Value']

            # Create a Payment record
            payment = Payment.objects.create(
                checkout_request_id=checkout_request_id,
                amount=amount,
                mpesa_receipt_number=mpesa_receipt_number,
                phone_number=phone_number,
                transaction_date=transaction_date,
                result_code=result_code,
                result_description=result_description
            )

            # Update order status based on the payment result
            try:
                order = Order.objects.get(checkout_request_id=checkout_request_id)
                if result_code == 0:  # Successful payment
                    order.status = 'confirmed'
                else:
                    order.status = 'failed'
                order.save()
            except Order.DoesNotExist:
                # Handle case where order doesn't exist
                return JsonResponse({'error': 'Order not found for the provided CheckoutRequestID'}, status=404)

            return JsonResponse({'message': 'Payment processed successfully'}, status=200)

        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': 'Invalid data received', 'details': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Order, Payment
from .forms import OrderStatusForm

def orders(request):
    # Fetch all orders
    orders = Order.objects.all()

    # Check payment status for each order
    for order in orders:
        # Find the payment that matches the order's checkout_request_id
        payment = Payment.objects.filter(checkout_request_id=order.checkout_request_id).first()
        
        if payment and payment.result_code == 0:  # Assuming result_code 0 indicates payment success
            order.is_paid = True  # Add a custom attribute to mark payment status
        else:
            order.is_paid = False  # Not paid or no payment found

    if request.method == 'POST':
        # Handle order status update if submitted
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        if order_id and new_status:
            # Update the order status
            order = get_object_or_404(Order, id=order_id)
            order.status = new_status
            order.save()

        # Redirect to the same page after updating the status
        return redirect('orders')

    return render(request, 'orders.html', {'orders': orders})


from django.conf import settings
import requests
import base64
from django.http import JsonResponse
from .models import Payment

# Function to generate the password
def generate_password():
    business_short_code = settings.DARAJA_BUSINESS_SHORT_CODE
    lipa_na_mpesa_online_passkey = settings.DARAJA_PASSKEY
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return encoded_password, timestamp

# Function to get the access token
def get_access_token():
    consumer_key = settings.DARAJA_CONSUMER_KEY
    consumer_secret = settings.DARAJA_CONSUMER_SECRET
    api_url = f"{"https://sandbox.safaricom.co.ke"}/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    access_token = response.json()['access_token']
    return access_token

# View to query the transaction status
def query_transaction_status(request, checkout_request_id):
    # Step 1: Generate the password
    password, timestamp = generate_password()

    # Step 2: Prepare the query request payload
    payload = {
        "BusinessShortCode": settings.DARAJA_BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id,
    }

    # Step 3: Send request to the Daraja Query API
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Choose the appropriate API URL based on the environment (Sandbox/Production)
    query_url = f"{"https://sandbox.safaricom.co.ke"}/mpesa/stkpushquery/v1/query"  # Use production URL in prod
    
    response = requests.post(query_url, json=payload, headers=headers)

    # Step 4: Process the response
    if response.status_code == 200:
        result = response.json()
        if result.get("ResponseCode") == "0" and result.get("ResultCode") == "0":
            # Transaction successful, update the Payment model
            payment = Payment.objects.get(checkout_request_id=checkout_request_id)
            payment.result_code = result.get("ResultCode")
            payment.result_description = result.get("ResultDesc")
            payment.save()

            return JsonResponse({"message": "Transaction successful", "status": "success", "data": result})
        else:
            return JsonResponse({"message": "Transaction failed", "status": "failed", "data": result})
    else:
        return JsonResponse({"message": "Failed to query transaction status", "status": "error"})
