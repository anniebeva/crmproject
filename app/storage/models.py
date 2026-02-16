from django.db import models

# Create your models here.
class Storage(models.Model):
    address = models.CharField(max_length=5000)
    company = models.OneToOneField(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='storage'
    )

    class Meta:
        verbose_name = 'Storage'
        verbose_name_plural = 'Storages'