from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from .models import Restaurant
from .serializers import RestaurantSerializer
from .models import Table, Category, Product, Restaurant
from .uploader import data_parser_and_saver 

from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes

import json


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/restaurants/
def restaurant_view(request):
    if request.method == 'GET':
        rest = Restaurant.objects.all()
        serializer = RestaurantSerializer(rest, many= True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['user'] = get_object_or_404(User, pk=data['user_id'])
        print(data)
        serializer = RestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        else:
            return JsonResponse(serializer.errors, status =400)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# /restaurant/
# Request Body: Auth, restaurant_id
def restaurant_detail(request):
    
    restaurant = get_object_or_404(Restaurant, pk=request.data['restaurant_id'])
    
    if request.method == 'GET':
        serializer = RestaurantSerializer(restaurant)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        restaurant.update(request)
        return JsonResponse(restaurant.to_dict())
    elif request.method == 'DELETE':
        restaurant.delete()
        return JsonResponse(status=204)

#  Categories///////////////////////////////////////////////////////////////////////

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/categories
# Request Body: GET: Auth,
#               POST: Auth, name, op(photo)
def category_view(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.filter(user=request.user).first()
        categories_q = Category.objects.filter(restaurant=restaurant)
        categories = []
        for category in categories_q:
            categories.append(category.to_dict())
        return JsonResponse(categories, safe=False)

    elif request.method == 'POST':
        data = {}
        data['restaurant'] = Restaurant.objects.filter(
            user=request.user).first()
        try:
            data['name'] = request.data['name']
        except(MultiValueDictKeyError):
            return JsonResponse({'Error': "Some Data Are NOT Provided"})

        if 'photo' in request.data.keys():
            file = data_parser_and_saver(request.data['photo'], tag='category')
            data['photo'] = str(file['directory'])
        else:
            data['photo'] = 'default.png'

        category = Category(name=data['name'], restaurant=data['restaurant'],
                            photo=data['photo'])
        category.save()
        return JsonResponse(category.to_dict())

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/category/
# Request Body: Auth, category_id
def category_detail(request):
    restaurant = Restaurant.objects.filter(user=request.user).first()
    category = get_object_or_404(Category, pk=request.data['category_id'], restaurant=restaurant)

    if request.method == 'GET':
        return JsonResponse(category.to_dict())
    elif request.method == 'PUT':
        category.update(request)
        return JsonResponse(category.to_dict())
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'details': "Deleted Successfully"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# restaurant/category/products/
# Request Body: Auth, category_id
def category_products(request):
    restaurant = Restaurant.objects.filter(user=request.user).first()
    category = Category.objects.filter(pk=request.data['category_id']).first()
    products_q = Product.objects.filter(
        category=category, restaurant=restaurant)
    products = []
    for product in products_q:
        products.append(product.to_dict())
    return JsonResponse(products, safe=False)

#  Products///////////////////////////////////////////////////////////////////////

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/products/
# Request Body: GET: Auth
#               POST: Auth, optionsjson, name, description, price, restaurant_id, category_id  
def product_view(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.filter(user=request.user).first()
        products_q = Product.objects.filter(restaurant=restaurant)
        products = []
        for product in products_q:
            products.append(product.to_dict())
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        data = {}
        try:
            data['optionsjson'] = json.loads(request.data['optionsjson'])
            data['name'] = request.data['name']
            data['description'] = request.data['description']
            data['price'] = request.data['price']
            data['restaurant'] = Restaurant.objects.filter(
                user=request.user).first()
            data['category'] = get_object_or_404(Category, pk=int(
                request.data['category_id']), restaurant=data['restaurant'])
        except(MultiValueDictKeyError):
            return JsonResponse({'Error': "Some Data Are NOT Provided"})

        if 'photo' in request.data.keys():
            file = data_parser_and_saver(request.data['photo'], tag='category')
            data['photo'] = str(file['directory'])
        else:
            data['photo'] = 'default.png'

        product = Product(name=data['name'], restaurant=data['restaurant'],
                            category=data['category'], price=float(
                            data['price']), optionsjson=data['optionsjson'],
                            description=data['description'], photo=data['photo'])
        product.save()
        return JsonResponse(product.to_dict(), status=201)
    
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/product/
# Request Body: Auth, product_id
def product_detail(request):
    restaurant = Restaurant.objects.filter(user=request.user).first()
    product = get_object_or_404(Product, pk=request.data['product_id'], restaurant=restaurant)

    if request.method == 'GET':
        return JsonResponse(product.to_dict())
    elif request.method == 'PUT':
        product.update(request)
        return JsonResponse(product.to_dict(), safe=False)
    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'details': "Deleted Successfully"})

#  Tables///////////////////////////////////////////////////////////////////////

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/tables/
# Request Body: Auth
def table_view(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.filter(user=request.user).first()
        tables_q = Table.objects.filter(restaurant=restaurant)
        tables = []
        for table in tables_q:
            tables.append(table.to_dict())
        return JsonResponse(tables, safe=False)

    elif request.method == 'POST':
        restaurant = Restaurant.objects.filter(user=request.user).first()
        tables = Table.objects.filter(restaurant=restaurant).all()
        table = Table(number= len(tables)+1, restaurant=restaurant)
        table.qr = table.qr_generator()
        table.save()
        return JsonResponse(table.to_dict())

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
# restaurant/table/
# Request Body: Auth, table_id
def table_detail(request):
    restaurant = Restaurant.objects.filter(user=request.user).first()
    table = get_object_or_404(Table, pk=request.data['table_id'], restaurant=restaurant)
    if request.method == 'GET':
        return JsonResponse(table.to_dict())
    elif request.method == 'PUT':
        table.update(request)
        return JsonResponse(table.to_dict())
    elif request.method == 'DELETE':
        tables = Table.objects.filter(restaurant=restaurant).all()
        for t in tables:
            if t.number > table.number:
                t.number = t.number-1
                t.save()
        table.delete()
        return JsonResponse({'details': "Deleted Successfully"})
    