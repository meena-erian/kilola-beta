from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from .models import Farmer, Buyer, Farm, Batch, Crop
from kilola import email_credentials


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')

    def get_type(self, data):
        has_farmer_profile = len(data.farmer_set.all()) > 0
        has_buyer_profile = len(data.buyer_set.all()) > 0
        if has_farmer_profile and not has_buyer_profile:
            return 'farmer'
        if has_buyer_profile and not has_farmer_profile:
            return 'buyer'
        if has_farmer_profile and has_buyer_profile:
            return 'buymer'
        else:
            return ''

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
            "user_permissions",
            "type"
        ]


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=500)
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
        password = validated_data['password']
        email = validated_data['email']
        type = validated_data['type']
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_active=False
        )
        user.set_password(password)
        user.save()
        mail_subject = 'Activate your Kilola account.'
        message = render_to_string('account_activation_email.html', {
            'user': user,
            'domain': 'kilola-beta.portacode.com',
            'token': default_token_generator.make_token(user),
            'uid': urlsafe_base64_encode(force_bytes(user.id))
        })
        email = EmailMessage(
            mail_subject,
            message,
            email_credentials.user,
            to=[email]
        )
        email.send(fail_silently=False)
        validated_data['status'] = 'SUCCESS'
        if type == 'farmer':
            Farmer.objects.create(user=user)
        elif type == 'buyer':
            Buyer.objects.create(user=user)
        return validated_data


class ConfirmEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(max_length=200)
    token = serializers.CharField(max_length=200)
    status = serializers.CharField(read_only=True)

    def create(self, data):
        uidb64 = data['uidb64']
        token = data['token']
        data['status'] = 'FAILED'
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            serializers.ValidationError('Invalid activation link')
        if user is not None and default_token_generator\
                .check_token(user, token):
            user.is_active = True
            user.save()
            data['status'] = 'SUCCESS'
        else:
            serializers.ValidationError('Invalid activation link')
        return data


class FarmerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Farmer
        fields = ['user']


class FarmSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer(read_only=True)

    class Meta:
        model = Farm
        fields = ['id', 'name', 'farmer', 'location', 'size']


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'crop', 'farm', 'area', 'weight', 'planting_date',
                  'harvesting_date', 'description']


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class BatchDetailsSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    farm = FarmSerializer(read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'crop', 'farm', 'area', 'weight', 'planting_date',
                  'harvesting_date', 'description']
