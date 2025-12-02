from django.contrib import admin
from .models import Route, Shop, Product, SaleRecord, SaleItem

# This allows managing "Sale Items" directly inside the "Sale Record" page
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1  # Shows one empty row by default

@admin.register(SaleRecord)
class SaleRecordAdmin(admin.ModelAdmin):
    # What columns to show in the list
    list_display = ('date', 'shop', 'rep', 'total_amount')
    # Sidebar filters (Crucial for analysis!)
    list_filter = ('date', 'rep', 'shop__route') 
    # Search bar
    search_fields = ('shop__name', 'rep__username')
    # Add the inline items table
    inlines = [SaleItemInline]

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'phone', 'owner_name')
    list_filter = ('route',)
    search_fields = ('name', 'address')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku_code', 'unit_price')
    search_fields = ('name', 'sku_code')

# Register the simple models
admin.site.register(Route)