from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_pct = models.FloatField(null=True, blank=True)
    availability_status = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    vendor = models.CharField(max_length=10)

    def __str__(self):
        return self.name