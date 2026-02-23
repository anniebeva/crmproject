from django.db import models
from django.db.models import ForeignKey

class Supply(models.Model):
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.CASCADE,
        related_name='supplies'
    )

    delivery_date = models.DateField()

    class Meta:
        verbose_name = 'Supply'
        verbose_name_plural = 'Supplies'



class SupplyProduct(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_item'
    )

    supply = models.ForeignKey(
        'supplies.Supply',
        on_delete=models.CASCADE,
        related_name='supply_item'
    )

    quantity = models.IntegerField()