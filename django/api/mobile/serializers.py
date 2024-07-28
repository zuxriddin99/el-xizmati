from rest_framework import serializers

from apps.users.validator import validate_uzbekistan_phone


class AuthSendSmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, default="+998911234567", validators=[validate_uzbekistan_phone])


class AuthVerifySmsSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, validators=[validate_uzbekistan_phone])
    code = serializers.CharField(max_length=10)
