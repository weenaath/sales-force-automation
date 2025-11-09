from decimal import Decimal
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SalesArea(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SalesRep(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales_rep')
    area = models.ForeignKey(SalesArea, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Product(models.Model):
    sku = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=200)
    default_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SalesEntry(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Credit'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    rep = models.ForeignKey(SalesRep, on_delete=models.PROTECT, related_name='sales_entries')
    area = models.ForeignKey(SalesArea, on_delete=models.PROTECT)
    customer_name = models.CharField(max_length=200, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    invoice_no = models.CharField(max_length=128, blank=True, null=True)
    payment_method = models.CharField(max_length=32, choices=PAYMENT_CHOICES, default='cash')
    notes = models.TextField(blank=True)
    admin_approved = models.BooleanField(default=False)
    commission_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    commission_amount = models.DecimalField(max_digits=14, decimal_places=2, editable=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['rep']),
            models.Index(fields=['area']),
        ]

    def save(self, *args, **kwargs):
        # Compute total and commission before saving
        self.total_amount = (Decimal(self.quantity) * Decimal(self.unit_price)).quantize(Decimal('0.01'))
        self.commission_amount = (self.total_amount * (Decimal(self.commission_pct) / Decimal(100))).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rep} | {self.total_amount} | {self.date}"
