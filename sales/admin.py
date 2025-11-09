from django.contrib import admin
from .models import SalesArea, SalesRep, Product, SalesEntry
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(SalesArea)
class SalesAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SalesRep)
class SalesRepAdmin(admin.ModelAdmin):
    list_display = ('user', 'area')
    search_fields = ('user__username','user__first_name','user__last_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','sku','default_unit_price','active')
    list_filter = ('active',)

@admin.register(SalesEntry)
class SalesEntryAdmin(admin.ModelAdmin):
    list_display = ('date','rep','area','product','total_amount','invoice_no','admin_approved')
    list_filter = ('admin_approved','date','area')
    search_fields = ('invoice_no','rep__user__username','customer_name')
    readonly_fields = ('total_amount','commission_amount','created_at')
