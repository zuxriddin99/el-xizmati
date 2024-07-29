from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.users.models import User
from apps.users.validator import validate_uzbekistan_phone


@extend_schema_field(OpenApiTypes.BINARY)
class CustomImageField(serializers.ImageField):
    pass


class AuthSendSmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, default="+998911234567", validators=[validate_uzbekistan_phone])


class AuthVerifySmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, validators=[validate_uzbekistan_phone])
    code = serializers.CharField(max_length=10)


class AuthUserSetInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    pasport_serial_number = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    photo = CustomImageField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "language",
            "pasport_serial_number",
            "role",
            "photo",
        ]
