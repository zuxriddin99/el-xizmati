import datetime
import re

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.ads.models import Category, AD, ADMedia
from apps.main.models import Region, District
from apps.users.models import User


class BaseResponseSerializer(serializers.Serializer):
    data = serializers.JSONField(default={}, required=False)
    error = serializers.JSONField(default={}, required=False)


class BasePaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField()
    total_objects = serializers.IntegerField()
    current_page_size = serializers.IntegerField()
    limit = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    results = serializers.ListField(child=serializers.DictField())


class TokensSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class AuthVerifyResponseSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    is_created = serializers.BooleanField()
    tokens = TokensSerializer()


class AuthVerifyResponseDataSerializer(BaseResponseSerializer):
    data = AuthVerifyResponseSerializer()


class AuthSetUserInfoResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo', 'passport_serial_number', 'role', 'phone_number')


class AuthSetUserInfoResponseDataSerializer(BaseResponseSerializer):
    data = AuthSetUserInfoResponseSerializer()


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon"]


class CategoriesPaginationSerializer(BasePaginationSerializer):
    results = CategoriesSerializer(many=True)


class CategoriesResponseSerializer(BaseResponseSerializer):
    data = CategoriesPaginationSerializer()


class RegionsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ["id", "name"]

    @staticmethod
    def get_name(obj):
        return obj.name_uz

class RegionsPaginationSerializer(BasePaginationSerializer):
    results = RegionsSerializer(many=True)


class RegionsResponseSerializer(BaseResponseSerializer):
    data = RegionsPaginationSerializer()


class DistrictsSerializer(serializers.ModelSerializer):
    region = RegionsSerializer()
    name = serializers.SerializerMethodField()
    class Meta:
        model = District
        fields = ["id", "name", "region"]

    @staticmethod
    def get_name(obj):
        return obj.name_uz


class DistrictsPaginationSerializer(BasePaginationSerializer):
    results = DistrictsSerializer(many=True)


class DistrictsResponseSerializer(BaseResponseSerializer):
    data = DistrictsPaginationSerializer()


class TESTJWTResponseSerializer(BaseResponseSerializer):
    data = TokensSerializer()

class ADMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADMedia
        fields = [
            "id",
            "file",
            "media_type",
        ]

class AdDetailSerializer(serializers.ModelSerializer):
    medias = ADMediaSerializer(many=True, source="ad_medias", required=False)

    class Meta:
        model = AD
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "price",
            "category",
            "work_type",
            "district",
            "latitude",
            "longitude",
            "address",
            "medias",
        ]


class ADDetailResponseSerializer(BaseResponseSerializer):
    data = AdDetailSerializer()
