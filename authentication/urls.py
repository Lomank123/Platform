from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from authentication.views import (
    FingerprintTokenObtainPairView,
    FingerprintTokenRefreshView,
    FingerprintTokenBlackListView,
)

app_name = "authentication"

urlpatterns = [
    path("obtain/", FingerprintTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", FingerprintTokenRefreshView.as_view(), name="token_refresh"),
    path("blacklist/", FingerprintTokenBlackListView.as_view(), name="token_blacklist"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
