from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
   
   
    # 1. def __str__(self):
    # The __str__ method in a Django model (or any Python class) is a special method that defines the string representation of an instance of the class.

    # When you call str(instance) or just try to print an instance of a model, Django will use the __str__ method to display the object.
    # In your Category model, the __str__ method is returning self.title. This means that when you print a Category object, the title of that category will be shown.
    def __str__(self):
        return self.title

    class Meta:
      # verbose_name_plural: This is telling Django what to use as the plural form of the model name. By default, Django will try to pluralize your model name automatically (e.g., Category would become Categorys or Categories).
      verbose_name_plural = "Categories"
        

class Product(models.Model):
    mainimage = models.ImageField(upload_to='Products')
    name = models.CharField(max_length=264)
    # this is in a Product model) and the Category model.
    # A Product can belong to one category, but a category can have many products (many-to-one relationship).
    # The ForeignKey stores the id of the related Category object in the Product table.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    detail_text = models.TextField(max_length=1000, verbose_name='Description')
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    
    
    # When is __str__ used?
    # Django Admin: When viewing objects in the Django admin panel, the __str__ method determines what is displayed for each object.
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created',]