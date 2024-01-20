from hashlib import sha256
from secrets import token_hex

from django.conf import settings

from authentication.exceptions import FingerprintException


class FingerprintService:
    """Provides methods to manage JWT fingerprint."""

    @staticmethod
    def generate_fingerprint():
        """Fingerprint should be stored in cookies."""
        return token_hex(32)

    @staticmethod
    def calculate_fingerprint_hash(fingerprint):
        """
        Hash is used for request validation.
        Should be stored in JWT access token payload.
        """
        return sha256(bytes(fingerprint, "utf-8")).hexdigest()

    def verify_fingerprint(self, request, payload):
        """
        Compare fingerprint hash from token payload and calculated hash from cookie.
        Raises FingerprintException if not they don't match.
        """
        cookie_fingerprint = request.COOKIES.get(settings.FINGERPRINT_COOKIE_NAME)
        payload_fingerprint_hash = payload.get("fingerprint_hash")

        if not cookie_fingerprint:
            raise FingerprintException("Fingerprint cookie not found")
        if not payload_fingerprint_hash:
            raise FingerprintException("Fingerprint hash not found")

        cookie_fingerprint_hash = self.calculate_fingerprint_hash(cookie_fingerprint)

        if cookie_fingerprint_hash != payload_fingerprint_hash:
            raise FingerprintException("Fingerprint hashes do not match")
