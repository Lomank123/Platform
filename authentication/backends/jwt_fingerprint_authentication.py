import logging

from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.exceptions import FingerprintException
from authentication.services import FingerprintService


class JWTFingerprintAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        # Validating fingerprint
        fingerprint_service = FingerprintService()

        try:
            fingerprint_service.verify_fingerprint(request, validated_token)
        except FingerprintException as ex:
            logging.exception(ex)
            return None

        return self.get_user(validated_token), validated_token
