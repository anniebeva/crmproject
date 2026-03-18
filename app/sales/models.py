from django.db import models
from django.db.models import ForeignKey
from decimal import Decimal

class Sale(models.Model):
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='sales'
    )

    buyer_name = models.CharField(max_length=256)
    sale_date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def apply(self):
        for sp in self.sales_items.all():
            sp.product.quantity -= sp.quantity
            sp.product.save()


    def rollback(self):
        for sp in self.sales_items.all():
            sp.product.quantity += sp.quantity
            sp.product.save()

    def delete(self, *args, **kwargs):
        self.rollback()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Sale #{self.id}, {self.buyer_name}'

class ProductSale(models.Model):
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_sale_items'
    )

    sale = models.ForeignKey(
        'sales.Sale',
        on_delete=models.CASCADE,
        related_name='sales_items'
    )

    quantity = models.PositiveIntegerField()

    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.price_at_sale is None:
            self.price_at_sale = self.product.sale_price * (1 - self.sale.discount / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.title} - {self.quantity} x ${self.price_at_sale}'