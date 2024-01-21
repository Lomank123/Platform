from django.urls import path

from authentication.views import (
    FingerprintTokenObtainPairView,
    FingerprintTokenRefreshView,
    FingerprintTokenBlackListView,
    FingerprintTokenVerifyView,
)

app_name = "authentication"

urlpatterns = [
    path("obtain/", FingerprintTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", FingerprintTokenRefreshView.as_view(), name="token_refresh"),
    path("blacklist/", FingerprintTokenBlackListView.as_view(), name="token_blacklist"),
    path("verify/", FingerprintTokenVerifyView.as_view(), name="token_verify"),
]
