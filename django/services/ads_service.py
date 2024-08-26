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
        return AD.objects.all()