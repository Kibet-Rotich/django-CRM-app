from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    # path('checkout',views.checkout,name='checkout'),
    path('payment',views.initiate_payment,name='initiate_payment'),
    path('payment_confirmation', views.payment_confirmation,name = "payment_confirmation"),
    path('orders',views.orders,name='orders'),
    path('payment/query/<str:checkout_request_id>/', views.query_transaction_status, name='query_transaction_status'),

    # path('login/', views.login_view, name='login'),
    # path('signup/', views.signup, name='signup'),
    # path('logout/', views.logout_view, name='logout'),
    # path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    # 
    # path('cart/updatequantity/<int:cart_item_id>/',views.update_cart_item_quantity,name = 'update_cart_item_quantity'),
    # 
    # path('order_confirmation/<int:order_id>/',views.order_confirmation,name='order_confirmation')
]
