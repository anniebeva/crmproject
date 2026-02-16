from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'INN', 'title')
    list_display_links = ('id', 'INN')
