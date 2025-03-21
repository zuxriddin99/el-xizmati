from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.ads.models import AD
from apps.chat.models import Message
from apps.users.models import User, UserRoleEnum
from apps.users.validator import validate_uzbekistan_phone


@extend_schema_field(OpenApiTypes.BINARY)
class CustomFileField(serializers.FileField):
    pass


class AuthSendSmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, default="+998911234567", validators=[validate_uzbekistan_phone])


class AuthVerifySmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, validators=[validate_uzbekistan_phone])
    code = serializers.CharField(max_length=10)


class AuthUserSetInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    passport_serial_number = serializers.CharField(required=True)
    photo = CustomFileField(required=True)
    role = serializers.ChoiceField(choices=UserRoleEnum.choices)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "language",
            "passport_serial_number",
            "role",
            "photo",
            "district",
        ]


class AdCreateSerializer(serializers.ModelSerializer):
    medias = serializers.ListField(child=CustomFileField(), required=False)

    class Meta:
        model = AD
        fields = [
            "name",
            "description",
            "price",
            "category",
            "work_type",
            "district",
            "address",
            "latitude",
            "longitude",
            "medias",
        ]


class GetUserJwtSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)


class SendOfferSerializer(serializers.Serializer):
    ad_id = serializers.IntegerField(required=True)


class UpdateOfferSerializer(serializers.Serializer):
    offer_id = serializers.IntegerField(required=True)


class SendMessageSerializer(serializers.ModelSerializer):
    medias = serializers.ListField(child=CustomFileField(), required=False)

    class Meta:
        model = Message
        fields = [
            "chat",
            "text",
            "parent",
            "medias",
        ]


class ChangeUserRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=UserRoleEnum.choices)


class UserUpdateSerializer(serializers.ModelSerializer):
    photo = CustomFileField(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "language",
            "photo",
            "district",
        ]
