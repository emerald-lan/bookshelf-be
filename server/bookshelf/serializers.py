from rest_framework import serializers
from .models import User, Book

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'is_active']

class BookSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = Book
		fields = '__all__'