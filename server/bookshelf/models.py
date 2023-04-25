from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)   
    avatar = models.ImageField(upload_to='images/users/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('id', 'is_superuser', 'username', 'email', 'is_active')

    def __str__(self):
        return self.username

class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    published_year = models.PositiveIntegerField()
    summary = models.TextField()
    image = models.ImageField(upload_to='images/books/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
