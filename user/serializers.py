from rest_framework import serializers
from django.contrib import auth
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from user.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    refresh_token = serializers.CharField(max_length=500, min_length=8, read_only=True)
    access_token = serializers.CharField(max_length=500, min_length=8, read_only=True)
    role = serializers.ListField(child=serializers.CharField(max_length=50), read_only=True)
    permissions = serializers.ListField(child=serializers.CharField(max_length=20), read_only=True)
    status = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_super_user = serializers.BooleanField(read_only=True)
    
    def get_is_super_user(self, value):
        print(value)
        return 'value.is_superuser'

    class Meta:
        model = User
        fields = ['email', 'password', 'refresh_token', 
                  'access_token', 'permissions', 'role', 'status', 'is_admin', 'is_super_user']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Credentials, try again!')
        if not user.is_active:
            raise AuthenticationFailed('Acccount disabled, please contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        user.last_login = timezone.now()
        user.save()
        tokens = user.get_tokens()
        
        data = dict(
                    access_token=tokens.get('access'), 
                    refresh_token=tokens.get('refresh'),
                    )   
        
        return data