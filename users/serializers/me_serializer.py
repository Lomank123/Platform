from rest_framework import serializers

from users.models import User


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "last_login",
            "date_joined",
        )
