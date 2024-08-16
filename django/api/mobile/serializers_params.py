from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.users.models import User
from apps.users.validator import validate_uzbekistan_phone


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(required=False)

class DistrictParamsSerializer(SearchSerializer):
    region = serializers.IntegerField(required=False)