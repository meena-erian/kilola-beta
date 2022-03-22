from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_text
# from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from .models import Farmer, Buyer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions"
        ]


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    type = serializers.CharField(
        max_length=200,
        help_text="User Type. Can be either of the string\
        values 'farmer' or 'buyer'"
    )
    status = serializers.CharField(read_only=True)

    def validate(self, data):
        # username = data['username']
        # first_name = data['first_name']
        # last_name = data['last_name']
        # email = data['email']
        type = data['type']
        if type not in ['farmer', 'buyer']:
            raise serializers.ValidationError(
                "Attribute 'type' must be either 'farmer' or 'buyer'"
            )
        return super().validate(data)

    def create(self, validated_data):
        username = validated_data['username']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        type = validated_data['type']
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=get_random_string(length=32),
            is_active=False
        )
        user.save()
        mail_subject = 'Activate your Kilola account.'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(
            mail_subject,
            message,
            'menas@portacode.com',
            to=[email]
        )
        email.send(fail_silently=False)
        validated_data['status'] = 'SUCCESS'
        if type == 'farmer':
            Farmer.objects.create(user=user)
        elif type == 'buyer':
            Buyer.objects.create(user=user)
        return validated_data
