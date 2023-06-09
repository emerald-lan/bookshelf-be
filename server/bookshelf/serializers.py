from rest_framework import serializers, exceptions
from .models import *

class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'phone_number', 'address', 'is_active', 'first_name', 'last_name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
