from rest_framework import serializers, exceptions
from .models import *

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        if (user.is_superuser != True):
            user.is_active = False
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'phone_number', 'address', 'is_active', 'first_name', 'last_name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context['request']

        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        validated_data['customer'] = user

        total = request.data.get('total')
        validated_data['total'] = total

        instance = super().create(validated_data)

        return instance

    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    def create(self, validated_data):
        request = self.context['request']

        book_id = request.data.get('book_id')
        book = Book.objects.get(id=book_id)
        validated_data['book_id'] = book_id

        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        validated_data['order_id'] = order_id

        instance = super().create(validated_data)

        return instance

    class Meta:
        model = OrderItem
        fields = '__all__'