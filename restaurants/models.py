from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

import qrcode

import json
import os
import random
import string

DOMAIN = "Domain.com"

from .uploader import data_parser_and_saver



class Restaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=1000, default='default.png')
    
    def to_dict(self):
        return {"restaurant_id":self.pk,"restaurant_name": self.name, "user_id":self.user.id,"image_url":"default.png"}
    def update(self, request):
        for i in request.data.keys():
            if i == 'name':
                self.name = request.data[i]
            elif i == 'photo':
                file = data_parser_and_saver(request.data[i], tag='category')
                self.photo = str(file['directory'])
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    photo = models.CharField(max_length=1000, default='default.png')
    
    def to_dict(self):
        return {'category_id':self.pk, 'category_name': self.name, 'category_photo': self.photo}
    def update(self, request):
        for i in request.data.keys():
            if i == 'category_name':
                self.name = request.data[i]
            elif i == 'category_photo':
                file = data_parser_and_saver(request.data[i], tag='category')
                self.photo = str(file['directory'])
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=50)

    description = models.CharField(max_length=300)

    price = models.DecimalField(max_digits=10000, decimal_places=2)

    photo = models.CharField(max_length=1000, default='default.png', null=True, blank=True)


    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def default_json():
        return {}
    def to_dict(self):
        return {'id':self.pk,'product_name': self.name, 'product_description':self.description, 'optionsjson':self.optionsjson,'product_price': self.price, 'product_photo': self.photo, 'category_id':self.category.pk}
    def update(self, request):
        for i in request.data.keys():
            if i == 'product_name':
                self.name = request.data[i]
            elif i == 'product_price':
                self.price = request.data[i]
            elif i == 'product_description':
                self.description = request.data[i]
            elif i == 'product_photo':
                file = data_parser_and_saver(request.data[i], tag='product')
                self.photo = str(file['directory'])
            elif i == 'category_id':
                restaurant =  Restaurant.objects.filter(user = request.user).first()
                self.category = get_object_or_404(Category, pk=int(request.data['category_id']), restaurant=restaurant)
            elif i == 'optionsjson':
                self.optionsjson = json.loads(request.data[i])
        self.save()
    optionsjson = models.JSONField(default=default_json)


class Table(models.Model):
    def qr_generator(self):
        qr  = "".join((random.choice(string.ascii_letters) for x in range(5))) 
        url = DOMAIN +"customer/table/" + str(self.restaurant.pk) + "/" + qr
        
        if not os.path.exists(f"qrs/{self.restaurant.pk}"):
            os.mkdir(f"qrs/{self.restaurant.pk}")
        
        qr_img = qrcode.make(url)
        qr_img.save(f"qrs/{self.restaurant.pk}/{qr}.png")
        return qr
    
    number = models.IntegerField()
    
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    qr = models.CharField(max_length=50, unique=True, auto_created=True)
    def to_dict(self):
        return {'id':self.pk, 'number': self.number, 'qr':self.qr, 'restaurant_id': self.restaurant.pk}

    def update(self, request):
        for i in request.data.keys():
            if i == 'number':
                self.number = request.data[i] 
        self.save()
