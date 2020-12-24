from django.contrib import admin
from .models import *
# Register your models here.


class ProductAdmin (admin.ModelAdmin):
    list_display = ['name', 'quantity']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Promotion)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(ShippingAddress)
