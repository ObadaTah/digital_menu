from django.urls import path
from .views import *

urlpatterns = [
    path('restaurants', restaurant_view), #All The Restaurant Details GET_POST
    path('', restaurant_detail), #All The Restaurant Details GET_PUT_DELETE
    
    path('categories', category_view),
    path('category', category_detail),
    path('category/products', category_products),
    
    path('products', product_view),
    path('product', product_detail),
    
    path('tables', table_view),
    path('table', table_detail),
    
]