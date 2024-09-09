from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm

from .models import Item

def index(request):
    # Retrieve all items from the database
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def cart(request):
    return render(request, 'cart_detail.html')


from .models import Location
def checkout(request):
    locations = Location.objects.all()  # Fetch all available locations
    return render(request, 'checkout.html', {'locations': locations})




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

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = float(request.POST.get('amount', 0))
        location_id = request.POST.get('location_id')

        if not phone_number or not amount or not location_id:
            return JsonResponse({'error': 'Phone number, amount, and location are required'}, status=400)

        # Find location and calculate total amount
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return JsonResponse({'error': 'Invalid location ID'}, status=400)
        
        delivery_price = location.delivery_price
        total_amount = amount + delivery_price

        # Create an order with location details and status
        order = Order.objects.create(
            amount=total_amount,
            phone_number=phone_number,
            status='pending',
            location=location
        )

        access_token = get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        business_short_code = settings.DARAJA_BUSINESS_SHORTCODE
        lipa_na_mpesa_online_passkey = settings.DARAJA_PASSKEY
        data_to_encode = business_short_code + lipa_na_mpesa_online_passkey + timestamp
        encoded_string = base64.b64encode(data_to_encode.encode())
        password = encoded_string.decode('utf-8')
        
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": total_amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.DARAJA_CALLBACK_URL,
            "AccountReference": str(order.id),
            "TransactionDesc": "Payment for order"
        }
        
        response = requests.post(api_url, json=payload, headers=headers)
        return JsonResponse(response.json())

    return HttpResponse(status=405)  # Method Not Allowed if not POST

import requests
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

@csrf_exempt
def payment_confirmation(request):
    if request.method == 'POST':
        # Extract payment confirmation data
        payment_data = request.POST.get("Body", {}).get("stkCallback", {})

        # Extract relevant fields
        result_code = payment_data.get("ResultCode")
        result_desc = payment_data.get("ResultDesc")
        callback_metadata = payment_data.get("CallbackMetadata", {}).get("Item", [])

        # Initialize variables
        amount = None
        transaction_id = None
        transaction_date = None
        phone_number = None
        account_reference = None

        # Extract fields from callback metadata
        for item in callback_metadata:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                transaction_id = item["Value"]
            elif item["Name"] == "TransactionDate":
                transaction_date = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phone_number = item["Value"]
            elif item["Name"] == "AccountReference":
                account_reference = item["Value"]

        # Validate the received data
        if not account_reference:
            return JsonResponse({'error': 'Missing AccountReference'}, status=400)
        if not transaction_id:
            return JsonResponse({'error': 'Missing Transaction ID'}, status=400)
        if not amount:
            return JsonResponse({'error': 'Missing Amount'}, status=400)
        if not phone_number:
            return JsonResponse({'error': 'Missing Phone Number'}, status=400)
        if not transaction_date:
            return JsonResponse({'error': 'Missing Transaction Date'}, status=400)

        try:
            # Find the corresponding order using the Account Reference
            order = Order.objects.get(id=account_reference)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        # Update the order status and save payment details
        if result_code == 0:  # assuming 0 indicates success
            order.status = 'completed'
        else:
            order.status = 'failed'

        order.transaction_id = transaction_id
        order.payment_amount = amount
        order.payment_phone_number = phone_number
        order.payment_time = datetime.strptime(str(transaction_date), "%Y%m%d%H%M%S")
        order.save()

        return JsonResponse({'result': 'Payment confirmation received and order updated'})

    return HttpResponse(status=405)  # Method Not Allowed if not POST
