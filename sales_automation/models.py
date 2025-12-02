from django.db import models
from django.contrib.auth.models import User

# 1. Routes (e.g., Homagama, Kottawa)
class Route(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# 2. Shops (The Customers)
class Shop(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=100, blank=True)
    address = models.TextField() 
    phone = models.CharField(max_length=15, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f"{self.name} ({self.route.name})"

# 3. Products (Siddhalepa Balm, etc.)
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku_code = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# 4. Sales Record (The Visit Header)
class SaleRecord(models.Model):
    rep = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sale #{self.id} - {self.shop.name}"

# 5. Sales Items (The specific products sold in a visit)
class SaleItem(models.Model):
    sale_record = models.ForeignKey(SaleRecord, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.price_at_sale:
            self.price_at_sale = self.product.unit_price
        super().save(*args, **kwargs)

    def get_subtotal(self):
        return self.quantity * self.price_at_sale