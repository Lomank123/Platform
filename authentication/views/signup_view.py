from rest_framework.generics import CreateAPIView

from authentication.serializers import SignupSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
