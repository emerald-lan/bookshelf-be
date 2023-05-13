from django.contrib import admin
from .models import User, Book, Order, OrderItem, Cart, Wishlist

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'is_active']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'published_year', 'unit_price', 'stock', 'cover', 'created_at', 'updated_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'admin_id', 'customer_name', 'customer_number', 'customer_address', 'status', 'total']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'book_id', 'quantity']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_id', 'quantity']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'book_id']