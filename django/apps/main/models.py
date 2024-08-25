from apps.base_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Region(BaseModel):
    name_oz = models.CharField(verbose_name="Uzbek kyril", max_length=150, default="")
    name_ru = models.CharField(verbose_name="Russian", max_length=150, default="")
    name_en = models.CharField(verbose_name="English", max_length=150, default="")
    name_uz = models.CharField(verbose_name="Uzbek latin", max_length=150, default="")

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name_plural = 'Regions'
        verbose_name = 'Region'
        ordering = ['name_en']
        db_table = 'regions'

    def get_name(self, language="en"):
        match language:
            case "en":
                return self.name_en
            case "ru":
                return self.name_ru
            case "oz":
                return self.name_oz
            case "uz":
                return self.name_uz
            case _:
                return self.name_uz


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name_oz = models.CharField(verbose_name="Uzbek kyril", max_length=150, default="")
    name_ru = models.CharField(verbose_name="Russian", max_length=150, default="")
    name_en = models.CharField(verbose_name="English", max_length=150, default="")
    name_uz = models.CharField(verbose_name="Uzbek latin", max_length=150, default="")

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name_plural = 'Districts'
        verbose_name = 'District'
        ordering = ['name_en']
        db_table = 'districts'

    def get_name(self, language="en"):
        match language:
            case "en":
                return self.name_en
            case "ru":
                return self.name_ru
            case "oz":
                return self.name_oz
            case "uz":
                return self.name_uz
            case _:
                return self.name_uz
