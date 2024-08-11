from apps.base_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'categories'


class WorkTypeEnum(models.TextChoices):
    ONE_TIME = "one_time", _("One Time Job")
    MANY_TIME = "many_time", _("Many Time Job")


class AD(BaseModel):
    owner = models.ForeignKey("users.User", related_name="owner_ads", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    district = models.ForeignKey("main.District", on_delete=models.CASCADE, related_name="district_ads")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_ads")
    work_type = models.CharField(max_length=20, choices=WorkTypeEnum.choices, default=WorkTypeEnum.ONE_TIME)

    def __str__(self):
        return self.name


def ad_media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/ad_<id>/<filename>
    return f"user_{instance.ad.owner_id}/ads/ad_{instance.ad_id}/{filename}"


class ADMedia(BaseModel):
    class MediaTypeEnum(models.TextChoices):
        image = "image", _("Image")
        video = "video", _("Video")

    ad = models.ForeignKey(AD, related_name="ad_medias", on_delete=models.CASCADE)
    file = models.FileField(upload_to=ad_media_directory_path)
    media_type = models.CharField(max_length=6, choices=MediaTypeEnum.choices, default=MediaTypeEnum.image)

    def __str__(self):
        return self.ad.name
