from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, BookSerializer
from .models import User, Book

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]