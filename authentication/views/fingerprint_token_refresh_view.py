import logging

import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase

from authentication.exceptions import FingerprintException
from authentication.serializers import FingerprintTokenRefreshSerializer
from authentication.services import FingerprintService


class FingerprintTokenRefreshView(TokenViewBase):
    """
    This implementation does not support
    refresh token rotation due to fingerprint.
    """

    serializer_class = FingerprintTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        access = request.data.get("access")
        payload = self.__get_payload(access)
        self.__verify_fingerprint(request, payload)
        context = {"fingerprint_hash": payload.get("fingerprint_hash")}
        serializer = self.get_serializer(
            data=request.data,
            context=context,
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Will return response with 401 status
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @staticmethod
    def __get_payload(access):
        """
        Return access token payload.

        Here we do not verify expiration since
        this token is definitely expired.
        """
        try:
            return jwt.decode(
                access,
                key=settings.SECRET_KEY,
                algorithms=[settings.SIMPLE_JWT.get("ALGORITHM")],
                options={"verify_exp": False},
            )
        except Exception as ex:
            logging.exception(ex)
            raise InvalidToken("Invalid access token")

    @staticmethod
    def __verify_fingerprint(request, payload):
        fingerprint_service = FingerprintService()

        try:
            fingerprint_service.verify_fingerprint(request, payload)
        except FingerprintException:
            raise APIException(
                detail="Wrong fingerprint",
                code=status.HTTP_401_UNAUTHORIZED,
            )
