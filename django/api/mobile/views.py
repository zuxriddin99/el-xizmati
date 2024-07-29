from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status

from api.views import GenericAPIView
from services.user_service import AuthService
from api.mobile import serializers
from api.mobile import serializers_response
from rest_framework.response import Response


class AuthAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    auth_service = AuthService()

    @extend_schema(
        tags=["auth"],
        request=serializers.AuthSendSmsSerializer,
        responses={
            status.HTTP_200_OK: serializers_response.BaseResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="send sms code for authentication",
        description="status=200 is meaning successfully sending email. After sending sms verify code via the url: "
                    "`/api/mobile/auth/verify-phone-number/`",
    )
    def send_sms(self, request, *args, **kwargs):
        serializer = serializers.AuthSendSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.auth_service.send_sms_to_phone(**serializer.validated_data)
        return Response({}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["auth"],
        request=serializers.AuthVerifySmsSerializer,
        responses={
            status.HTTP_200_OK: serializers_response.AuthVerifyResponseDataSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Verify phone number",
        description="Verifing phone number with code",
    )
    def verify_phone_number(self, request, *args, **kwargs):
        serializer = serializers.AuthVerifySmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.auth_service.verify_phone_number(**serializer.validated_data)
        result = self.get_response_data(serializers_response.AuthVerifyResponseSerializer, data)
        return Response(result, status=status.HTTP_200_OK)

    # @extend_schema(
    #     tags=["auth"],
    #     request=serializers.AuthVerifySmsSerializer,
    #     responses={
    #         status.HTTP_200_OK: serializers_response.AuthVerifyResponseDataSerializer,
    #         status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
    #     },
    #     summary="Verify phone number",
    #     description="Verifing phone number with code",
    # )
    # def set_user_info(self, request, *args, **kwargs):
    #     serializer = serializers.AuthUserSetInfoSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = self.request.user
    #     data = self.auth_service.set_user_info(user=user, **serializer.validated_data)
    #     result = self.get_response_data(serializers_response.AuthVerifyResponseSerializer, data)
    #     return Response(result, status=status.HTTP_200_OK)
