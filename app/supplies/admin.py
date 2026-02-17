from django.contrib import admin
from .models import Supply

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_id', 'delivery_date']
    list_display_links = ['id', 'supplier_id']

