from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    ConfirmEmailSerializer,
    UserFarmSerializer,
    UserBatchSerializer
)
from .models import Farm, Batch
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.serializers import ValidationError


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


class ConfirmEmailView(generics.CreateAPIView):
    serializer_class = ConfirmEmailSerializer

    def post(self, request):
        return self.create(request)


class UserFarmView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserFarmSerializer

    def get_queryset(self):
        return Farm.objects.filter(farmer__user=self.request.user)

    def perform_create(self, serializer):
        farmer = self.request.user.farmer_set.all()
        if not len(farmer):
            raise ValidationError(
                'Seems like authenticated user is not a farmer')
        serializer.save(farmer=farmer[0])

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class UserBatchView(
        generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserBatchSerializer

    def get_queryset(self):
        return Batch.objects.filter(farm__farmer__user=self.request.user)

    def perform_create(self, serializer):
        farmer = self.request.user.farmer_set.all()
        if not len(farmer):
            raise ValidationError(
                'Seems like authenticated user is not a farmer')
        farm = serializer.validated_data['farm']
        if farm.farmer.user != self.request.user:
            raise ValidationError(
                'You don\'t own this farm'
            )
        serializer.save()

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
