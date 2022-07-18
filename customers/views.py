from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Order, Item
from restaurants.models import Restaurant, Category, Product, Table
from rest_framework.parsers import JSONParser, MultiPartParser

from rest_framework.decorators import api_view, parser_classes
import json

@api_view(['GET'])
# customer/table/{restaurant_id}/{qr}/
def customer_menu(request, restaurant_id, qr):
    if request.method == 'GET':
        table = get_object_or_404(
            Table, qr=qr, restaurant_id=restaurant_id)
        categories_q = Category.objects.filter(restaurant=restaurant_id)
        categories = []
        categories.append(
            {'restaurant': table.restaurant.to_dict(), 'table_number': table.number, 'table_id': table.id})
        # Add Logo URL
        for category in categories_q:
            categories.append(category.to_dict())
        return JsonResponse(categories, safe=False)


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
# /customer/category/products
# Request Body : restaurant_id, category_id.
def get_customers_category_products(request):
    restaurant = get_object_or_404(
        Restaurant, pk=request.data['restaurant_id'])
    category = get_object_or_404(
        Category, pk=request.data['category_id'], restaurant=restaurant)
    products_q = Product.objects.filter(
        category=category, restaurant=restaurant).all()
    products = []
    for i in range(len(products_q)):
        products.append(products_q[i].to_dict())
    return JsonResponse(products, safe=False)


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
# customer/order/create
# Request Body: restaurant_id, table_id
def order_create(request):
    restaurant = get_object_or_404(
        Restaurant, pk=request.data["restaurant_id"])
    table = get_object_or_404(Table, pk=request.data["table_id"])
    new_order = Order(restaurant_id=restaurant, table=table)
    new_order.save()
    response = {'order': new_order.to_dict(), 'items': []}
    return JsonResponse(response, safe=False)


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
# /order/view/
# Request Body: order_id
def order_view(request):
    order = get_object_or_404(Order, pk=request.data["order_id"])
    items_q = Item.objects.filter(order=order.pk).all()
    response = {'order': order.to_dict(), 'items': []}
    for item in items_q:
        response['items'].append(item.to_dict())
    return JsonResponse(response, safe=False)


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
# /item/add/
# Request Body: order_id, product_id, notes, options, price
def add_item(request):
    product = Product(pk=int(request.data["product_id"]))
    order = Order(pk=int(request.data["order_id"]))
    item = Item(notes = request.data['notes'],options= request.data['options'], price= int(request.data['price']), product= product, order= order)
    item.save()
    return JsonResponse({"saved item id: " : item.id})


@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
# /items/add/
# Request Body: order_id, [product_id, notes, options, price]
def add_items(request):
    order = Order(pk=int(request.data["order_id"]))
    for i in request.data['items']:
        product = Product(pk=int(i['product_id']))
        item = Item(notes = i['notes'],options= i['options'], price= int(i['price']), product= product, order=order)
        item.save()
    return JsonResponse({"items were added to the order": True}, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, JSONParser])
# /item/detail/
# Request Body: order_id, item_id
def item_detail(request):
    item = get_object_or_404(
        Item, pk=request.data['item_id'], order=request.data['order_id'])
    if request.method == 'GET':
        return JsonResponse(item.to_dict())
    elif request.method == 'PUT':
        item.update(request)
        return JsonResponse(item.to_dict())
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'details': "Item Deleted Successfully"})


@api_view(['POST', "GET"])
@parser_classes([MultiPartParser, JSONParser])
# /order/status/
# Request Body: order_id
def order_status(request):
    order = get_object_or_404(Order, pk=request.data["order_id"])
    if request.method == 'GET':
        return JsonResponse({"order_status": order.status}, safe=False)
    if request.method == 'POST':
        order.status = request.data['status']
        order.save()
        return JsonResponse({"order_status": order.status}, safe=False)
