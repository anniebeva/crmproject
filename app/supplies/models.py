from django.db import models

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

