from rest_framework import serializers, exceptions
from .models import *

class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # Kiểm tra username đã tồn tại hay chưa
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists. Please try a different username.")

        # Kiểm tra email đã tồn tại hay chưa
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists. Please try a different email.")

        # Kiểm tra mật khẩu
        password = data.get('password')
        repeated_password = self.initial_data.get('repeatedPassword')
        # print(password)
        # print(repeated_password)
        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data
    
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
