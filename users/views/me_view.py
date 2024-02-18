from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.serializers import MeSerializer


class MeView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(data=serializer.data)
