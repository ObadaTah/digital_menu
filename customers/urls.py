from django.urls import path
from .views import *

urlpatterns = [
    path('table/<int:restaurant_id>/<str:qr>/', customer_menu),
    
    path('category/products/', get_customers_category_products),

    path('item/add/', add_item), 
    path('items/add/', add_items), 
    path('item/detail/', item_detail), 

    path('order/create/', order_create), 
    path('order/view/', order_view), 
    path('order/status/', order_status),

    
    
]