from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    vendor = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["name", "price", "vendor"])]

    def __str__(self):
        return self.name
