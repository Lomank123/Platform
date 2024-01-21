from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class FingerprintTokenRefreshSerializer(serializers.Serializer):
    """
    This implementation does not support
    refresh token rotation due to fingerprint.
    """

    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        access = refresh.access_token
        access["fingerprint_hash"] = self.context.get("fingerprint_hash")
        return {"access": str(access)}
