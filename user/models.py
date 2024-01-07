from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=20, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
    # @property
    # def password():
    #     raise AttributeError('Password is not callable.')
    
    # @password.setter
    # def password(self, password):
    #     """Hash user password"""
    #     hash_password = make_password(password)
    #     self.password = hash_password
    #     self.save()

