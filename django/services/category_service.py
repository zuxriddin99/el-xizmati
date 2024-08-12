from apps.ads.models import Category


class CategoryService:

    @staticmethod
    def get_categories():
        return Category.objects.all()
