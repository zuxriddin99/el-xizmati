# import django_filters
from random import choices

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


class AdsFilter(SearchFilter):
    ordering = filters.ChoiceFilter(method="filter_ordering")

    @staticmethod
    def filter_search(queryset, name, value):
        return (
            queryset
            .filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(district__name_oz__icontains=value) |
                Q(district__name_ru__icontains=value) |
                Q(district__name_en__icontains=value) |
                Q(district__name_uz__icontains=value) |
                Q(district__region__name_oz__icontains=value) |
                Q(district__region__name_ru__icontains=value) |
                Q(district__region__name_en__icontains=value) |
                Q(district__region__name_uz__icontains=value)
            )
        )

    @staticmethod
    def filter_ordering(queryset, name, value):
        match value:
            case "created_at":
                return queryset.order_by("created_at")
            case "-created_at":
                return queryset.order_by("-created_at")
            case "most_viewed":
                pass  # todo need to add order via most viewed
                # return queryset.order_by("-created_at")
            case "most_rated":
                pass  # todo need to add order via most rated
                # return queryset.order_by("-created_at")
        return queryset
