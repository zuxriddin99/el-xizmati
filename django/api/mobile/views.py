from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.mobile import serializers, serializers_response, serializers_params
from api.mobile.filters import DistrictsFilter, RegionsFilter, AdsFilter, WorkerOffersFilter
from api.views import GenericAPIView
from conf.pagination import CustomPagination
from services.address_service import RegionService, DistrictService
from services.ads_service import AdsService
from services.category_service import CategoryService
from services.chat_service import ChatService, MessageService
from services.notification_service import NotificationService
from services.offer_service import OfferService
from services.test_service import GetJwtService
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


class RegionsAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    region_service = RegionService()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegionsFilter

    @extend_schema(
        tags=["addresses"],
        parameters=[serializers_params.SearchSerializer],
        responses={
            status.HTTP_200_OK: serializers_response.RegionsResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Regions list",
        description="Regions list",
    )
    def regions_list(self, request, *args, **kwargs):
        regions = self.region_service.get_regions()
        filtered_queryset = self.filter_queryset(regions)

        result = self.get_response_data(
            serializer_class=serializers_response.RegionsSerializer,
            instance=filtered_queryset,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)


class DistrictAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    district_service = DistrictService()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistrictsFilter

    @extend_schema(
        tags=["addresses"],
        parameters=[serializers_params.DistrictParamsSerializer],
        responses={
            status.HTTP_200_OK: serializers_response.DistrictsResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Districts list",
        description="Districts list",
    )
    def districts_list(self, request, *args, **kwargs):
        districts = self.district_service.get_districts()
        filtered_queryset = self.filter_queryset(districts)
        result = self.get_response_data(
            serializer_class=serializers_response.DistrictsSerializer,
            instance=filtered_queryset,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)


class ADSAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    ads_service = AdsService()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdsFilter

    @extend_schema(
        tags=["ads"],
        request={"multipart/form-data": serializers.AdCreateSerializer},
        responses={
            status.HTTP_201_CREATED: serializers_response.ADDetailResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Ads create",
        description="Ads create",
    )
    def ads_create(self, request, *args, **kwargs):
        serializer = serializers.AdCreateSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        ad = self.ads_service.ad_create_service(user=user, **serializer.validated_data)
        result = self.get_response_data(
            serializer_class=serializers_response.AdDetailSerializer,
            instance=ad,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["ads"],
        parameters=[serializers_params.AdsListSerializer],
        responses={
            status.HTTP_201_CREATED: serializers_response.ADListResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Ads list",
        description="Ads list",
    )
    def ads_list(self, request, *args, **kwargs):
        serializer = serializers_params.AdsListSerializer(data=request.GET, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        ads = self.ads_service.get_ads_list()
        filtered_queryset = self.filter_queryset(ads)
        result = self.get_response_data(
            serializer_class=serializers_response.AdListSerializer,
            instance=filtered_queryset,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["ads"],
        responses={
            status.HTTP_201_CREATED: serializers_response.ADDetailResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Ads detail",
        description="Ads detail",
    )
    def ads_detail(self, request, *args, **kwargs):
        ad_pk = kwargs.get("pk")
        user = request.user
        ad = self.ads_service.get_ad_detail(owner_id=user.id, ad_pk=ad_pk)
        result = self.get_response_data(
            serializer_class=serializers_response.AdDetailSerializer,
            instance=ad,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)


class TestAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    test_service = GetJwtService()

    @extend_schema(
        tags=["test"],
        request={"application/json": serializers.GetUserJwtSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.TESTJWTResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Get jwt",
        description="Get jwt",
    )
    def get_jwt(self, request, *args, **kwargs):
        serializer = serializers.GetUserJwtSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        tokens = self.test_service.get_jwt(user_id)
        result = self.get_response_data(
            serializer_class=serializers_response.TokensSerializer,
            instance=tokens,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)


class OfferAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    offer_service = OfferService()

    @extend_schema(
        tags=["offers"],
        request={"application/json": serializers.SendOfferSerializer},
        responses={
            status.HTTP_201_CREATED: serializers_response.SendOfferResponseDataSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Send offer",
        description="Send offer",
    )
    def send_offer(self, request, *args, **kwargs):
        serializer = serializers.SendOfferSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        ad_id = serializer.validated_data["user_id"]
        user_id = request.user.id
        offer = self.offer_service.send_offer(ad_id=ad_id, user_id=user_id)
        result = self.get_response_data(
            serializer_class=serializers_response.SendOfferResponseSerializer,
            instance=offer,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["offers"],
        request={"application/json": serializers.UpdateOfferSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.BaseResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Accept offer",
        description="Accept offer",
    )
    def accept_offer(self, request, *args, **kwargs):
        serializer = serializers.UpdateOfferSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        offer_id = serializer.validated_data["offer_id"]
        user_id = request.user.id
        self.offer_service.accept_offer(offer_id=offer_id, user_id=user_id)
        return Response({}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["offers"],
        request={"application/json": serializers.UpdateOfferSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.BaseResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Cancel offer",
        description="Cancel offer",
    )
    def cancel_offer(self, request, *args, **kwargs):
        serializer = serializers.UpdateOfferSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        offer_id = serializer.validated_data["offer_id"]
        user_id = request.user.id
        self.offer_service.cancel_offer(offer_id=offer_id, user_id=user_id)
        return Response({}, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["offers"],
        request={"application/json": serializers.UpdateOfferSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.BaseResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Complete offer",
        description="Complete offer",
    )
    def complete_offer(self, request, *args, **kwargs):
        serializer = serializers.UpdateOfferSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        offer_id = serializer.validated_data["offer_id"]
        user_id = request.user.id
        self.offer_service.complete_offer(offer_id=offer_id, user_id=user_id)
        return Response({}, status=status.HTTP_200_OK)


class WorkerOfferAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    offer_service = OfferService()
    filter_backends = [DjangoFilterBackend]
    filterset_class = WorkerOffersFilter

    @extend_schema(
        tags=["offers"],
        parameters=[serializers_params.WorkerOffersFilterSerializer],
        responses={
            status.HTTP_200_OK: serializers_response.WorkerOfferResponseDataSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Worker offers list",
        description="Worker offers list",
    )
    def offers_list(self, request, *args, **kwargs):
        user_id = request.user.id
        offers = self.offer_service.get_worker_offers(user_id=user_id)
        filtered_queryset = self.filter_queryset(offers)
        result = self.get_response_data(
            serializer_class=serializers_response.WorkerOfferListSerializer,
            instance=filtered_queryset,
            context=self.get_serializer_context(),
            many=True
        )
        return Response(result, status=status.HTTP_200_OK)


class ChatAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    chat_service = ChatService()

    @extend_schema(
        tags=["chats"],
        request={"application/json": serializers.SendOfferSerializer},
        responses={
            status.HTTP_200_OK: serializers_response.ChatListResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Chats list",
        description="Chats list",
    )
    def chats_list(self, request, *args, **kwargs):
        user = request.user
        chats = self.chat_service.chats_list(request_user=user)

        result = self.get_response_data(
            serializer_class=serializers_response.ChatsListResponseSerializer,
            instance=chats,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)


class MessageAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    msg_service = MessageService()

    @extend_schema(
        tags=["chats"],
        request={"multipart/form-data": serializers.SendMessageSerializer},
        responses={
            status.HTTP_201_CREATED: serializers_response.MessageCreateResponseDataSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Message create",
        description="Message create",
    )
    def send_message(self, request, *args, **kwargs):
        serializer = serializers.SendMessageSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = request.user
        message = self.msg_service.create_message(user=user, **serializer.validated_data)
        result = self.get_response_data(
            serializer_class=serializers_response.MessageCreateResponseSerializer,
            instance=message,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
        tags=["chats"],
        parameters=[serializers_params.PaginationSerializer],
        responses={
            status.HTTP_200_OK: serializers_response.MessageListResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="Messages list",
        description="Messages list",
    )
    def messages_list(self, request, *args, **kwargs):
        chat_id = kwargs.get("pk")
        messages = self.msg_service.get_messages(chat_id=chat_id)
        context = self.get_serializer_context()
        context["user_id"] = request.user.id
        result = self.get_response_data(
            serializer_class=serializers_response.MessageSerializer,
            instance=messages,
            many=True,
            context=context
        )
        return Response(result, status=status.HTTP_200_OK)


class NotificationAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    notification_service = NotificationService()

    @extend_schema(
        tags=["notifications"],
        responses={
            status.HTTP_200_OK: serializers_response.NotificationResponseSerializer,
            status.HTTP_400_BAD_REQUEST: serializers_response.BaseResponseSerializer,
        },
        summary="User notifications",
        description="Message create",
    )
    def notifications_list(self, request, *args, **kwargs):
        user = request.user
        notifications = self.notification_service.user_notifications(user=user)
        result = self.get_response_data(
            serializer_class=serializers_response.NotificationSerializer,
            instance=notifications,
            many=True,
            context=self.get_serializer_context()
        )
        return Response(result, status=status.HTTP_200_OK)

