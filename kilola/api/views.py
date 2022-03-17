from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        return self.list(request)