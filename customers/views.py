from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Order, Item
from restaurants.models import Restaurant, Category, Product, Table


from rest_framework.decorators import api_view


@api_view(['GET'])
# customer/table/{restaurant_id}/{qr}/
def customer_menu(request, restaurant_id, qr):
    if request.method == 'GET':
        table = get_object_or_404(
            Table, qr=qr, restaurant_id=restaurant_id)
        categories_q = Category.objects.filter(restaurant=restaurant_id)
        categories = []
        categories.append(
            {'restaurant': table.restaurant.to_dict(), 'table_number': table.number})
        # Add Logo URL
        for category in categories_q:
            categories.append(category.to_dict())
        return JsonResponse(categories, safe=False)


@api_view(['GET'])
# /customer/category/products
# Request Body : restaurant_id, category_id.
def get_customers_category_products(request):
    print('request')
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


@api_view(['GET'])
# customer/order/create
# Request Body: restaurant_id, table_id
def order_create(request):
    restaurant = get_object_or_404(
        Restaurant, pk=request.data["restaurant_id"])
    table = get_object_or_404(Table, pk=request.data["table_id"])
    new_order = Order(restaurant=restaurant, table=table)
    new_order.save()
    response = {'order': new_order.to_dict(), 'items': []}
    return JsonResponse(response, safe=False)


@api_view(['GET'])
# /order/view/
# Request Body: order_id
def order_view(request):
    order = get_object_or_404(Order, pk=request.data["order_id"])
    items_q = Item.objects.filter(order=order.pk).all()
    response = {'order': order.to_dict(), 'items': []}
    for item in items_q:
        response['items'].append(item.to_dict())
    return JsonResponse(response, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
# /order/detail/
# Request Body: order_id, item_id
def order_detail(request):
    item = get_object_or_404(
        Item, pk=request.data['item_id'], order=request.data['order_id'])
    if request.method == 'GET':
        return JsonResponse(item.to_dict())
    elif request.method == 'PUT':
        item.update(request.data)
        return JsonResponse(item.to_dict())
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({'details': "Item Deleted Successfully"})


@api_view(['GET'])
# /order/submit/
# Request Body: order_id
def order_submit(request):
    order = get_object_or_404(Order, pk=request.data["order_id"])
    order.update({status: 1})
    return JsonResponse(response, safe=False)


@api_view(['GET'])
# /order/received/
# Request Body: order_id
def order_received(request):
    order = get_object_or_404(Order, pk=request.data["order_id"])
    order.update({status:4 })
    return JsonResponse(response, safe=False)
