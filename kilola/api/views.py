from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response


class UserAPIView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = self.request.user
        user_data = get_object_or_404(queryset, pk=user.pk)
        return Response(UserSerializer(user_data).data)
