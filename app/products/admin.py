from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quantity', 'storage_id')
    list_display_links = ('id', 'title', 'storage_id')
