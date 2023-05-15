from rest_framework import viewsets, permissions
from bookshelf.serializers import UserSerializer, BookSerializer, OrderSerializer, OrderItemSerializer, CartSerializer, WishlistSerializer
from .models import User, Book, Order, OrderItem, Cart, Wishlist

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
