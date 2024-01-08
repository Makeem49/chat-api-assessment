from rest_framework import serializers
from django.contrib import auth
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from rest_framework.exceptions import AuthenticationFailed
from user.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    refresh_token = serializers.CharField(max_length=500, min_length=8, read_only=True)
    access_token = serializers.CharField(max_length=500, min_length=8, read_only=True)
    
    
    def get_is_super_user(self, value):
        print(value)
        return 'value.is_superuser'

    class Meta:
        model = User
        fields = ['refresh_token', 'access_token', 'password', 'email']

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
    
    
class LogoutSerializer(serializers.Serializer):
    refresh_token =  serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise ValidationError({'incorrect_token': 'The token is either invalid or expired'})
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
    def get_username(self, obj):
        if not obj.username:
            return obj.first_name
        return obj.username
    
    
    