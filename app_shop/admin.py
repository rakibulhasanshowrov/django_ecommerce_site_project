from django.contrib import admin
from app_shop.models import Category, Product
# Register your models here.

# This line registers the Category model with the Django admin interface. Once registered, Django will automatically generate a basic CRUD (Create, Read, Update, Delete) interface for the Category model in the admin panel.

# After registering the Category model, you'll be able to manage categories through the Django admin panel. You can add new categories, view existing ones, edit, and delete them.
admin.site.register(Category)
admin.site.register(Product)
