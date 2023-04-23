from django.db import models

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
