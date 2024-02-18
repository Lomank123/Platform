from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from django.conf import settings


class FingerprintTokenBlackListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenBlacklistSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        # Delete fingerprint from cookies
        response.delete_cookie(settings.FINGERPRINT_COOKIE_NAME)
        return response
