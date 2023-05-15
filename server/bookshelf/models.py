from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(validators=[EmailValidator()])
    avatar = models.ImageField(upload_to='images/users/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', 'is_superuser', 'username', 'email', 'is_active')

    def __str__(self):
        return self.username
    
class Admin(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.is_superuser = True
        super().save(*args, **kwargs)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    published_year = models.PositiveIntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='images/books/', blank=True, null=True)
    unit_price = models.PositiveIntegerField(blank=True, default=0)
    stock = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id', 'title', 'author', 'category', 'published_year', 'unit_price', 'stock', 'created_at', 'updated_at')

    def __str__(self):
        return self.title
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',to_field='id')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_orders', null=True,to_field='id')
    customer_name = models.CharField(max_length=100)
    customer_number = models.CharField(max_length=20)
    customer_address = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"Order {self.id} - Customer {self.customer_id.username}"

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items',to_field='id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    multi_unit_price = models.PositiveIntegerField()
    def __str__(self):
        return f"Order Item {self.id} - Order {self.order.id} - Book {self.book.title}"
    
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts',to_field='id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE,to_field='id')
    quantity = models.PositiveIntegerField()
    multi_unit_price = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Cart {self.id} - User {self.user_id.username} - Book {self.book_id.title}"


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists',to_field='id')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE,to_field='id')

    def __str__(self):
        return f"Wishlist {self.id} - User {self.user_id.username} - Book {self.book_id.title}"
