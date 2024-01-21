from django.urls import path, include

from authentication.views import (
    FingerprintTokenObtainPairView,
    FingerprintTokenRefreshView,
    FingerprintTokenBlackListView,
    FingerprintTokenVerifyView,
    SignupView,
)

app_name = "authentication"

token_urlpatterns = [
    path("obtain/", FingerprintTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", FingerprintTokenRefreshView.as_view(), name="token_refresh"),
    path("blacklist/", FingerprintTokenBlackListView.as_view(), name="token_blacklist"),
    path("verify/", FingerprintTokenVerifyView.as_view(), name="token_verify"),
]

auth_urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
]

urlpatterns = [
    path("token/", include(token_urlpatterns)),
    path("", include(auth_urlpatterns)),
]
