from django.contrib import admin
from .models import User, Book

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_superuser', 'username', 'email', 'password', 'avatar', 'is_active')

admin.site.register(Book)