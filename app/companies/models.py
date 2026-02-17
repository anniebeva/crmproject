from django.db import models
from authenticate.models import User
from django.utils import timezone
from django.conf import settings

class Company(models.Model):
    INN = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.title
