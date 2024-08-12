from api.mobile.views import AuthAPIView, CategoriesAPIView
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
]
