from django.db import models

class Supplier(models.Model):
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='suppliers'
    )

    title = models.CharField(max_length=200)
    INN = models.CharField(max_length=12, unique=True)

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.title
