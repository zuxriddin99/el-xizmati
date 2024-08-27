from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.users.models import User
from apps.users.validator import validate_uzbekistan_phone

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    limit = serializers.IntegerField(default=10)

class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)

class DistrictParamsSerializer(SearchSerializer, PaginationSerializer):
    region = serializers.IntegerField(required=False)

class AdsListSerializer(SearchSerializer, PaginationSerializer):
    region = serializers.IntegerField(required=False)
    district = serializers.IntegerField(required=False)
    ordering = serializers.ChoiceField(choices=["created_at", "-created_at", "most_viewed", "most_rated"], required=False)