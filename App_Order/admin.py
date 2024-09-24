from django.contrib import admin
from App_Order.models import Cart, Order

# Register your models here.

admin.site.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'purchased', 'created', 'updated', 'get_total')
admin.site.register(Order)