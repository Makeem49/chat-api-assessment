from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager."""
    
    def create_user(self, email, password, **extra_fields):
        """
        Use email, password, and the additional fields to create and save user objects.
        """
        if not email:
            raise TypeError('User must have an email')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_verified = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        """
        Use email, password, and the additional fields to create and save superuser objects.
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True

        user.save()
        return user
