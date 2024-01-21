from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenViewBase

from authentication.exceptions import FingerprintException
from authentication.serializers import FingerprintTokenVerifySerializer


class FingerprintTokenVerifyView(TokenViewBase):
    serializer_class = FingerprintTokenVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request},
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # Will return response with 401 status
            raise InvalidToken(e.args[0])
        except FingerprintException as ex:
            raise InvalidToken(str(ex))

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
