from api.mobile.views import AuthAPIView, CategoriesAPIView, DistrictAPIView, RegionsAPIView, ADSAPIView, TestAPIView, \
    OfferAPIView, WorkerOfferAPIView, ChatAPIView, MessageAPIView, NotificationAPIView, UserAPIView
from django.urls import include, path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

app_name = "mobile"
urlpatterns = [
    # Device
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

    # Authentication
    path("auth/send-sms/", AuthAPIView.as_view({"post": "send_sms"}), name="auth"),
    path("auth/verify-phone-number/", AuthAPIView.as_view({"post": "verify_phone_number"}), name="auth-verify"),
    path("auth/set-user-info/", AuthAPIView.as_view({"post": "set_user_info"}), name="auth-set-user-info"),

    # Category
    path("categories/", CategoriesAPIView.as_view({"get": "categories_list"}), name="categories"),

    # Address
    path("districts/", DistrictAPIView.as_view({"get": "districts_list"}), name="districts"),
    path("regions/", RegionsAPIView.as_view({"get": "regions_list"}), name="regions"),

    # AD
    path("ads/", ADSAPIView.as_view({"post": "ads_create", "get": "ads_list"}), name="ads"),
    path("ads/<int:pk>/", ADSAPIView.as_view({"get": "ads_detail", }), name="ad-detail"),

    # Offer
    path("offer/send/", OfferAPIView.as_view({"post": "send_offer"}), name="send_offer"),
    path("offer/accept/", OfferAPIView.as_view({"post": "accept_offer"}), name="accept_offer"),
    path("offer/cancel/", OfferAPIView.as_view({"post": "cancel_offer"}), name="cancel_offer"),
    path("offer/complate/", OfferAPIView.as_view({"post": "complete_offer"}), name="complete_offer"),
    path("worker/offers/", WorkerOfferAPIView.as_view({"get": "offers_list"}), name="offers_list"),

    # Chat
    path("chats/", ChatAPIView.as_view({"get": "chats_list"})),
    path("chats/messages/", MessageAPIView.as_view({"post": "send_message"})),
    path("chats/<int:pk>/messages/", MessageAPIView.as_view({"get": "messages_list"})),

    # Test routes
    path("test/get-token/", TestAPIView.as_view({"post": "get_jwt"}), name="test"),

    # Notification
    path("notifications/", NotificationAPIView.as_view({"get": "notifications_list"}), name="notifications"),

    # User
    path("user/change-role/", UserAPIView.as_view({"post": "change_role"})),
]
