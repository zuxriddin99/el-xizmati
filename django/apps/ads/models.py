from apps.base_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    icon = models.FileField(upload_to="categories/", null=True)
    name_oz = models.CharField(verbose_name="Uzbek kyril", max_length=150, default="")
    name_ru = models.CharField(verbose_name="Russian", max_length=150, default="")
    name_en = models.CharField(verbose_name="English", max_length=150, default="")
    name_uz = models.CharField(verbose_name="Uzbek latin", max_length=150, default="")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name_uz

    class Meta:
        ordering = ('order',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'categories'

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


class WorkTypeEnum(models.TextChoices):
    ONE_TIME = "one_time", _("One Time Job")
    MANY_TIME = "many_time", _("Many Time Job")


class AD(BaseModel):
    owner = models.ForeignKey("users.User", related_name="owner_ads", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_ads")
    work_type = models.CharField(max_length=20, choices=WorkTypeEnum.choices, default=WorkTypeEnum.ONE_TIME)
    district = models.ForeignKey("main.District", on_delete=models.CASCADE, related_name="district_ads")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(default="", max_length=300, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def ad_media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/ad_<id>/<filename>
    return f"user_{instance.ad.owner_id}/ads/ad_{instance.ad_id}/{filename}"


class ADMedia(BaseModel):
    class MediaTypeEnum(models.TextChoices):
        IMAGE = "image", _("Image")
        VIDEO = "video", _("Video")

    ad = models.ForeignKey(AD, related_name="ad_medias", on_delete=models.CASCADE)
    file = models.FileField(upload_to=ad_media_directory_path)
    media_type = models.CharField(max_length=6, choices=MediaTypeEnum.choices, default=MediaTypeEnum.IMAGE)

    def __str__(self):
        return self.ad.name


class OfferStatus(models.TextChoices):
    NEW = "new", _("New")
    PROCESSING = "processing", _("Processing")
    COMPLETED = "completed", _("Completed")
    CANCELED = "canceled", _("Canceled")


class Offer(BaseModel):
    status = models.CharField(choices=OfferStatus.choices, default=OfferStatus.NEW, max_length=10)
    ad = models.ForeignKey(AD, related_name="ad_offers", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", related_name="user_offers", on_delete=models.CASCADE)
    worker_was_completed = models.BooleanField(default=False)
    owner_was_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.status

    class Meta:
        db_table = "offers"
        unique_together = (("user", "ad"),)
