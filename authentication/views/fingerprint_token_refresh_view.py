from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase
from django.conf import settings

from authentication.serializers import FingerprintTokenRefreshSerializer
from authentication.services import FingerprintService


class FingerprintTokenRefreshView(TokenViewBase):
    """
    This implementation does not support
    refresh token rotation due to fingerprint.
    """

    serializer_class = FingerprintTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        cookie_fingerprint = request.COOKIES.get(settings.FINGERPRINT_COOKIE_NAME)

        if not cookie_fingerprint:
            raise APIException(
                detail="Fingerprint cookie not found",
                code=status.HTTP_401_UNAUTHORIZED,
            )

        # TODO: Change logic: receive outdated access token,
        #  check fingerprint and only then update it
        fingerprint_service = FingerprintService()
        fingerprint_hash = fingerprint_service.calculate_fingerprint_hash(
            cookie_fingerprint
        )
        serializer = self.get_serializer(
            data=request.data,
            context={"fingerprint_hash": fingerprint_hash},
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Will return response with 401 status
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
