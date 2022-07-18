from django.db import models
from restaurants.models import Restaurant, Product, Table
import json
# Create your models here.

class Order(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)

    table = models.ForeignKey(Table, on_delete=models.CASCADE)

    total = models.DecimalField(default=0.00, max_digits=10000, decimal_places=2)

    CHOICES = [
        (0, 'Ordering'),
        (1,'Submited'),
        (2,'Opened'),
        (3,'Ready'),
        (4,'Received'),
        (5,'Paid'),
    ]

    status = models.IntegerField(
        choices=CHOICES,
        default=0,
    )
    def to_dict(self):
        return {'id':self.pk,'status':self.status,'total': self.total}
    
    def update(self, request):
        for i in request.data.keys():
            if i == 'total':
                self.total = request.data[i]
            if i == 'status':
                self.status = request.data[i]
        self.save()



class Item(models.Model):
    notes = models.CharField(max_length=1000)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
 
    options = models.CharField(max_length=50, null=True, blank=True)

    price = models.DecimalField(max_digits=10000, decimal_places=2, default=0.0)
    def to_dict(self):
        return {'id':self.pk,'notes':self.notes,'product_id': self.product.id, 'options': self.options, 'price': self.price}

    def update(self, request):
        for i in request.data.keys():
            if i == 'notes':
                self.notes = request.data[i]
            elif i == 'options':
                self.options = request.data[i]
            elif i == 'price':
                self.price = request.data[i]
        self.save()
