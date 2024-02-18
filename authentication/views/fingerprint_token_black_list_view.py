from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.views import TokenViewBase
from django.conf import settings


class FingerprintTokenBlackListView(TokenViewBase):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenBlacklistSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.delete_cookie(settings.FINGERPRINT_COOKIE_NAME)
        return response
