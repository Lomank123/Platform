from datetime import timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from django.conf import settings

from authentication.serializers import FingerprintTokenObtainPairSerializer
from authentication.services import FingerprintService


class FingerprintTokenObtainPairView(TokenViewBase):
    serializer_class = FingerprintTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        fingerprint_service = FingerprintService()
        fingerprint = fingerprint_service.generate_fingerprint()
        fingerprint_hash = fingerprint_service.calculate_fingerprint_hash(fingerprint)
        data = {
            "fingerprint_hash": fingerprint_hash,
            **request.data,
        }
        serializer = self.get_serializer(
            data=data,
            context={"fingerprint_hash": fingerprint_hash},
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Will return response with 401 status
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.JWT_FINGERPRINT.get("FINGERPRINT_COOKIE_NAME"),
            value=fingerprint,
            max_age=timedelta(
                days=settings.JWT_FINGERPRINT.get("FINGERPRINT_COOKIE_MAX_AGE_IN_DAYS")
            ),
            domain=settings.JWT_FINGERPRINT.get("FINGERPRINT_COOKIE_DOMAIN"),
            secure=not settings.DEBUG,
            httponly=True,
            samesite="strict",
        )

        return response
