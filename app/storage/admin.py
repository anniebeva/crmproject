from django.contrib import admin

from .models import Storage

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'company_id')
    list_display_links = ('id', 'address', 'company_id')
