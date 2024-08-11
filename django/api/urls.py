from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("mobile/", include("api.mobile.urls", namespace="mobile")),
]
