from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    photo = serializers.CharField()
    user = serializers.ReadOnlyField(source='user.id')
    
    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
