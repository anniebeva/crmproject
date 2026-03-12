from django.contrib import admin
from .models import Sale, SaleProduct

class SaleProductInline(admin.TabularInline):
    model = SaleProduct
    readonly_fields = ('price_at_sale', 'total_price')
    fields = ('product', 'quantity', 'price_at_sale', 'total_price')
    extra = 0

    def total_price(self, obj):
        price = obj.price_at_sale or 0
        qty = obj.quantity or 0
        return price * qty

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_id', 'buyer_name', 'sale_date']
    list_display_links = ['id', 'company_id']
    list_filter = ['sale_date', 'company__title']

    inlines = [SaleProductInline]


