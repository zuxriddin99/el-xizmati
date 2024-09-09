from rest_framework import exceptions

from apps.ads.models import Category, AD, ADMedia
from apps.users.models import User


class AdsService:

    @staticmethod
    def ad_create_service(user: User, **val_data):
        medias = val_data.pop("medias", [])
        ad = AD.objects.create(owner=user, **val_data)
        for i in medias:
            media_type = i.content_type.split("/")[0]
            ADMedia.objects.create(ad=ad, media_type=media_type, file=i)
        return ad

    @staticmethod
    def get_categories():
        return Category.objects.all()

    @staticmethod
    def get_ads_list():
        return AD.objects.filter(is_active=True).order_by("-created_at")

    @staticmethod
    def get_ad_detail(owner_id: int, ad_pk: int):
        try:
            return AD.objects.get(pk=ad_pk, owner_id=owner_id)
        except AD.DoesNotExist:
            raise exceptions.NotFound(f"Ad: {ad_pk} not found", code="not_found")
