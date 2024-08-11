from apps.base_app.models import BaseModel
from django.db import models


# Create your models here.
class Region(BaseModel):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Regions'
        verbose_name = 'Region'
        ordering = ['name']
        db_table = 'regions'


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Districts'
        verbose_name = 'District'
        ordering = ['name']
        db_table = 'districts'
