from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company_id', 'INN')
    list_display_links = ('id', 'title', 'company_id', 'INN')

