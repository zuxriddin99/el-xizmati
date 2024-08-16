# import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters


class SearchFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    @staticmethod
    def filter_search(queryset, name, value):
        return queryset.filter(Q(name__icontains=value))


class DistrictsFilter(SearchFilter):
    region = filters.CharFilter(method="filter_region")

    @staticmethod
    def filter_region(queryset, name, value):
        return queryset.filter(region_id=int(value))


class RegionsFilter(SearchFilter):
    pass
