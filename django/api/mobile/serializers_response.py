import datetime
import re
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from fcm_django.models import FCMDevice
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class BaseResponseSerializer(serializers.Serializer):
    data = serializers.JSONField(default={}, required=False)
    error = serializers.JSONField(default={}, required=False)


class TokensSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class AuthVerifyResponseSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    is_created = serializers.BooleanField()
    tokens = TokensSerializer()


class AuthVerifyResponseDataSerializer(BaseResponseSerializer):
    data = AuthVerifyResponseSerializer()

# class AuthSetUserInfoResponseSerializer(serializers.Serializer):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')