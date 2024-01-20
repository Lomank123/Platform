from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class FingerprintTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        """Here we add the fingerprint hash into the access token."""

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token

        access["fingerprint_hash"] = self.context.get("fingerprint_hash")
        data["refresh"] = str(refresh)
        data["access"] = str(access)

        return data
