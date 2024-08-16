from apps.main.models import Region, District


class RegionService:

    @staticmethod
    def get_regions():
        return Region.objects.all()


class DistrictService:

    @staticmethod
    def get_districts():
        return District.objects.all().select_related("region")
