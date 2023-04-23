from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'url', 'username', 'email', 'password', 'is_active', 'is_superuser']

class BookSerializer(serializers.HyperlinkedModelSerializer):
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = Book
		fields = '__all__'