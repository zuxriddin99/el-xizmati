from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status

from api.views import GenericAPIView
from services.user_service import AuthService
from api.mobile import serializers
from rest_framework.response import Response


class AuthAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    auth_service = AuthService()

    @extend_schema(
        tags=["auth"],
        request=serializers.AuthSendSmsSerializer,
        summary="send sms code for authentication",
        description="After sending sms verify code via the url: `/api/mobile/auth/verify-phone-number/`",
    )
    def send_sms(self, request, *args, **kwargs):
        serializer = serializers.AuthSendSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        self.auth_service.send_sms_to_phone(phone_number=phone_number)
        return Response({}, status=status.HTTP_200_OK)
