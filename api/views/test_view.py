from rest_framework.views import APIView, Response
from rest_framework import status

from django.conf import settings


class TestView(APIView):
    @staticmethod
    def get(request):
        data = {
            "status": "OK",
            "cookie_fingerprint": str(
                request.COOKIES.get(settings.FINGERPRINT_COOKIE_NAME)
            ),
            "auth_headers": str(request.headers.get("Authorization")),
        }

        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )
