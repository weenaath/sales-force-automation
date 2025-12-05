from django.contrib import admin
from .models import Route, Shop, Product, SaleRecord, SaleItem, RepProfile
from django.utils.html import format_html

# This allows managing "Sale Items" directly inside the "Sale Record" page
class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1  # Shows one empty row by default

@admin.register(SaleRecord)
class SaleRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'shop', 'rep', 'total_amount', 'view_location') # Added view_location
    list_filter = ('date', 'rep', 'shop__route')
    search_fields = ('shop__name', 'rep__username')
    inlines = [SaleItemInline]

    # Function to generate Google Maps Link
    def view_location(self, obj):
        if obj.gps_lat and obj.gps_lon:
            url = f"https://www.google.com/maps/search/?api=1&query={obj.gps_lat},{obj.gps_lon}"
            return format_html('<a href="{}" target="_blank" style="color:blue;">View Map 📍</a>', url)
        return "No Data"
    
    view_location.short_description = "GPS Location"

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

@admin.register(RepProfile)
class RepProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_target')