from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.EmailField(validators=[EmailValidator()], blank=False, null=False, unique=True)
    avatar = models.ImageField(upload_to='images/users/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, validators=[MinLengthValidator(10), MaxLengthValidator(15)], blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username

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
    
    def __str__(self):
        return self.title

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return f"Order {self.id} - Customer {self.customer.username}"

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(blank=True, default=0)


    def __str__(self):
        return f"Order Item {self.id} - Order {self.order.id} - Book {self.book.id}"
