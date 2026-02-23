from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    storage = models.ForeignKey(
        'storage.Storage',
        on_delete=models.CASCADE,
        related_name='products'
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'









