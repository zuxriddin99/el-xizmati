import datetime
import re

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.ads.models import Category, AD, ADMedia, Offer
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
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon"]


    def get_name(self, obj):
        language = self.context["request"].headers.get('Accept-Language', 'en')
        return obj.get_name(language)



class CategoriesPaginationSerializer(BasePaginationSerializer):
    results = CategoriesSerializer(many=True)


class CategoriesResponseSerializer(BaseResponseSerializer):
    data = CategoriesPaginationSerializer()


class RegionsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ["id", "name"]

    def get_name(self, obj):
        language = self.context["request"].headers.get('Accept-Language', 'en')
        return obj.get_name(language)



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

    def get_name(self, obj):
        language = self.context["request"].headers.get('Accept-Language', 'en')
        return obj.get_name(language)


class AdDistrictsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = ["id", "name"]

    def get_name(self, obj):
        language = self.context["request"].headers.get('Accept-Language', 'en')
        return obj.get_name(language)


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


class ADOwnerSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(default=0)
    quantity_ads = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "photo",
            "created_at",
            "quantity_ads",
            "rating",
        ]


class AdListSerializer(serializers.ModelSerializer):
    owner = ADOwnerSerializer()
    district = AdDistrictsSerializer()

    class Meta:
        model = AD
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "price",
            "work_type",
            "district",
            "created_at",
        ]

class ADListPaginationResponseSerializer(BasePaginationSerializer):
    results = AdListSerializer(many=True)


class ADListResponseSerializer(BaseResponseSerializer):
    data = ADListPaginationResponseSerializer()


class SendOfferResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            "id",
            "status",
            "ad",
        ]


class SendOfferResponseDataSerializer(BaseResponseSerializer):
    data = SendOfferResponseSerializer()


class OfferAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD
        fields = [
            "id",
            "name",
            "description",
            "price",
        ]

class WorkerOfferListSerializer(serializers.ModelSerializer):
    ad = OfferAdSerializer(required=True)
    class Meta:
        model = Offer
        fields = [
            "id",
            "status",
            "ad"
        ]

class WorkerOfferListPaginationSerializer(BasePaginationSerializer):
    results = WorkerOfferListSerializer(many=True)

class WorkerOfferResponseDataSerializer(BaseResponseSerializer):
    data = WorkerOfferListPaginationSerializer()