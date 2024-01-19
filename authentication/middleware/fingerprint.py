import logging

from django.http import JsonResponse
from django.utils import timezone
import jwt

from django.conf import settings

from django.contrib.auth import get_user_model
from jwt import PyJWTError

# from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger(__name__)


class FingerprintMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        start_time = timezone.now()

        is_auth_required_request = not any(
            request.path.startswith(path) for path in settings.AUTH_EXCLUDED_PATHS
        )

        if is_auth_required_request:
            try:
                token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
                algorithms = [settings.SIMPLE_JWT.get("ALGORITHM")]
            except Exception as ex:
                logger.exception(ex)
                return JsonResponse(
                    {"error": "Authorization error occurred"}, status=403
                )

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=algorithms)
            except PyJWTError as ex:
                logger.exception(ex)
                return JsonResponse({"error": str(ex)}, status=403)

            user_model = get_user_model()
            user_id = payload.get("user_id")

            try:
                user = user_model.objects.get(id=user_id)
            except user_model.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            logger.warning(payload)
            logger.warning(user)

        # Call
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        total_time = timezone.now() - start_time
        logger.warning(f"Time taken: {total_time.total_seconds()} seconds")

        return response
