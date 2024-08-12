from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.mobile import serializers, serializers_response
from api.views import GenericAPIView
from conf.pagination import CustomPagination
from services.category_service import CategoryService
from services.user_service import AuthService


class AuthAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    auth_service = AuthService()

    # parser_classes = [MultiPartParser]

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

    @extend_schema(
        tags=["auth"],
        request={'multipart/form-data': serializers.AuthUserSetInfoSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.AuthSetUserInfoResponseDataSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="set user information",
        description="Set user information",
    )
    def set_user_info(self, request, *args, **kwargs):
        serializer = serializers.AuthUserSetInfoSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        data = self.auth_service.set_user_info(user=user, **serializer.validated_data)
        result = self.get_response_data(serializers_response.AuthSetUserInfoResponseSerializer, data,
                                        context=self.get_serializer_context())
        return Response(result, status=status.HTTP_200_OK)


class CategoriesAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    categories_service = CategoryService()
    # parser_classes = [MultiPartParser]

    @extend_schema(
        tags=["categories"],
        request=None,
        responses={
            status.HTTP_200_OK: serializers_response.CategoriesResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Categories list",
        description="Categories list",
    )
    def categories_list(self, request, *args, **kwargs):
        categories = self.categories_service.get_categories()

        result = self.get_response_data(
            serializer_class=serializers_response.CategoriesSerializer,
            instance=categories,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)
