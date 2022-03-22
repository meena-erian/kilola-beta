from django.contrib.auth.models import User
from .serializers import UserSerializer, SignUpSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics


class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = self.request.user
        user_data = get_object_or_404(queryset, pk=user.pk)
        return Response(self.serializer_class(user_data).data)


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        return self.create(request)
