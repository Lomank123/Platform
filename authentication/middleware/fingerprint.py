import logging

import jwt

from django.conf import settings
from django.http import JsonResponse

from jwt import PyJWTError
from rest_framework import status

from authentication.exceptions import FingerprintException
from authentication.services import FingerprintService


class FingerprintMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_auth_required_request = not any(
            request.path.startswith(path) for path in settings.AUTH_EXCLUDED_PATHS
        )

        if is_auth_required_request:
            try:
                algorithms = [settings.SIMPLE_JWT.get("ALGORITHM")]
                access_token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
                payload = jwt.decode(
                    access_token, settings.SECRET_KEY, algorithms=algorithms
                )
                fingerprint_service = FingerprintService()
                fingerprint_service.verify_fingerprint(request, payload)
            except PyJWTError as ex:
                return JsonResponse(
                    data={"error": str(ex)},
                    status=status.HTTP_403_FORBIDDEN,
                )
            except FingerprintException as ex:
                return JsonResponse(
                    data={"error": str(ex)},
                    status=status.HTTP_403_FORBIDDEN,
                )
            except Exception as ex:
                logging.exception(ex)
                return JsonResponse(
                    data={"error": "Authorization error occurred"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        response = self.get_response(request)

        return response
