from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken

from authentication.services import FingerprintService


class FingerprintTokenVerifySerializer(TokenVerifySerializer):
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        super().validate(attrs)

        token = UntypedToken(attrs["token"])
        payload = token.payload
        request = self.context.get("request")
        fingerprint_service = FingerprintService()
        fingerprint_service.verify_fingerprint(request, payload)

        return {}
