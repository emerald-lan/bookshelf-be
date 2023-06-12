from rest_framework import serializers, exceptions
from .models import *

class UserSerializer(serializers.ModelSerializer):

    # def validate(self, data):
    #     user_id = self.instance.id if self.instance else None

    #     username = data.get('username', None)
    #     if User.objects.filter(username=username).exclude(id=user_id).exists():
    #         raise serializers.ValidationError("Username already exists. Please try a different username.")

    #     # Kiểm tra email đã tồn tại hay chưa
    #     email = data.get('email', None)
    #     if User.objects.filter(email=email).exclude(id=user_id).exists():
    #         raise serializers.ValidationError("Email already exists. Please try a different email.")

    #     # Kiểm tra mật khẩu
    #     password = data.get('password', None)
    #     repeated_password = self.initial_data.get('repeatedPassword')
    #     # print(password)
    #     # print(repeated_password)
    #     if repeated_password and password != repeated_password:
    #         raise serializers.ValidationError("Passwords do not match.")

    #     first_name = data.get('first_name', None)
    #     last_name = data.get('last_name', None)
    #     if not first_name or not last_name:
    #         raise serializers.ValidationError("Please enter your full name.")

    #     return data

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['firstName'],
    #         last_name=validated_data['lastName'],
    #         password=validated_data['password']
    #     )
    #     return user
    
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.avatar = validated_data.get('avatar', instance.avatar)
    #     instance.phone_number = validated_data.get('phone_number', instance.phone_number)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.save()
    #     return instance
    
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
