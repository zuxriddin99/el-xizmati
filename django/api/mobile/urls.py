from django.urls import include, path

from api.mobile.views import AuthAPIView

app_name = "mobile"
urlpatterns = [
    path("auth/send-sms/", AuthAPIView.as_view({"post": "send_sms"}), name="auth"),
    path("auth/verify-phone-number/", AuthAPIView.as_view({"post": "verify_phone_number"}), name="auth-verify"),
    # path("auth/set-user-info/", AuthAPIView.as_view({"post": "verify_phone_number"}), name="auth-verify"),
]
