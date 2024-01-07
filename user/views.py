# new imports
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import AllowANyUser
from .serializers import (
                        LoginSerializer,
                        RegistrationSerializer, 
                        )
# Create your views here.
class RegistrationView(AllowANyUser, generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.validated_data
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    
class LoginView(AllowANyUser, generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)