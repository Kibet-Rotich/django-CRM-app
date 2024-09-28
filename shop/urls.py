from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    # path('checkout',views.checkout,name='checkout'),
    path('payment',views.initiate_payment,name='initiate_payment'),
    path('payments/', views.payment_list, name='payment_list'),
    path('payment_confirmation', views.payment_confirmation,name = "payment_confirmation"),
    path('orders',views.orders,name='orders'),
    path('payment/query/<str:checkout_request_id>/', views.query_transaction_status, name='query_transaction_status'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('login/', views.login_view, name='login'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:item_id>/edit/', views.item_update, name='item_update'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/add/', views.location_create, name='location_create'),
    path('locations/<int:location_id>/edit/', views.location_update, name='location_update'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout_view, name='logout'),
    # path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    # 
    # path('cart/updatequantity/<int:cart_item_id>/',views.update_cart_item_quantity,name = 'update_cart_item_quantity'),
    # 
    # path('order_confirmation/<int:order_id>/',views.order_confirmation,name='order_confirmation')
]
