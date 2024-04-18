from compartidos.models import TimestampedModel

# Librerías de Terceros
from django.contrib.gis.db import models


class Product(TimestampedModel):
    product_name = models.CharField(
        max_length=50, verbose_name="Product Name", unique=True
    )
    description = models.CharField(max_length=500)
    stock = models.IntegerField(verbose_name="Stock Quantity")
    expiry_date = models.DateTimeField(verbose_name="Expiry Date")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Alarm(TimestampedModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product"
    )
    alert_type = models.CharField(max_length=20, verbose_name="Alert Type")
    alert_date = models.DateField(verbose_name="Alert Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_expired = models.BooleanField(default=False, verbose_name="Is Expired")

    def __str__(self):
        return f"{self.product.product_name} - {self.alert_type}"

    class Meta:
        verbose_name = "Alarm"
        verbose_name_plural = "Alarms"
