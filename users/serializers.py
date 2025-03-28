from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for registering new users.

        Validates passwords and ensures that they match before creating the user account.
    """
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields=[
            'id',
            'username',
            'email',
            'password',
            'confirm_password'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Customized serializer for obtaining JWT tokens.

        Ensures that only verified users can log in and obtain tokens.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verified:
            raise ValidationError("Your email is not verified.")

        return data