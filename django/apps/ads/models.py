from apps.base_app.models import BaseModel
from django.db import models

# Create your models here.


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'categories'


# class AD(BaseModel):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=0)
