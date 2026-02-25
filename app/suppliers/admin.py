from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'INN', 'title', 'company_id')
    list_display_links = ('id', 'title', 'company_id', 'INN')

