from rest_framework import serializers
from .models import User, Book, Order, OrderItem, Cart, Wishlist

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'is_active']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
	def create(self, validated_data):
		user = User.objects.create_user(
			email = validated_data['email'],
			username = validated_data['username'],
			password = validated_data['password']
		)
		return user

	class Meta:
		model = User
		fields = ['url', 'email', 'username', 'password']