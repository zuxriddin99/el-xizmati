from apps.ads.models import Category, AD
from apps.users.models import User


class AdsService:

    @staticmethod
    def ad_create_service(user: User, **val_data):
        pass

    @staticmethod
    def get_categories():
        return Category.objects.all()
