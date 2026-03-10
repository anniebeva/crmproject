from django.contrib import admin
from .models import Supply, SupplyProduct


class SupplyProductInline(admin.TabularInline):
    model = SupplyProduct
    extra = 1

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_id', 'delivery_date']
    list_display_links = ['id', 'supplier_id']
    list_filter = ['delivery_date', 'supplier__company']

    inlines = [SupplyProductInline]

