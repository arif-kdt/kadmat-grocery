from django.db import models
from django.conf import settings
from products.models import BaseProduct

class Shop(models.Model):
    seller = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    location = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SellerProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['shop', 'base_product']

    def __str__(self):
        return f"{self.base_product.name} - {self.shop.name}"

class ProductVariant(models.Model):
    UNIT_CHOICES = [
        ('count', 'Count (pieces)'),
        ('gram_250', '250g'),
        ('gram_500', '500g'),
        ('kg_1', '1kg'),
        ('kg_2', '2kg'),
        ('litre_1', '1 Litre'),
        ('custom', 'Custom'),
    ]
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='variants')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    custom_unit = models.CharField(max_length=50, blank=True)
    quantity_per_unit = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def get_unit_display_name(self):
        if self.unit == 'count':
            return f"{self.quantity_per_unit} pieces"
        elif self.unit == 'custom':
            return self.custom_unit
        return self.get_unit_display()

    def __str__(self):
        return f"{self.seller_product} - {self.get_unit_display_name()} - ₹{self.price}"