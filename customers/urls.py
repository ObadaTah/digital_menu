from django.urls import path
from .views import *

urlpatterns = [
    path('table/<int:restaurant_id>/<str:qr>', customer_menu),
    
    path('category/products', get_customers_category_products),

    path('order/create', order_create), 
    path('order/view', order_view), 
    path('order/detail', order_detail), 
    path('orders/submit', order_submit),
    path('order/received', order_received),

    
    
]