from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, name, password=None):
        """Create a ner user profile"""

        #Verify user EmailField
        if not email:
            raise ValueError("Every user must have an email address")

        #normalize the email address
        email = self.normalize_email(email)
        #Create the user objects
        user = self.model(email=email, name=name)

        #Set password and hash it automagically
        user.set_password(password)

        #save user
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create a new user and assign it the Admin(Super) privileges in PermissionMixin"""

        #Create a normal user by calling the create_user function in the class
        user = self.create_user(email, name, password)

        #Assign user privilege using PermissionsMixin
        user.is_superuser = True
        user.is_staff = True

        #Save user
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for user of the app"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name"""
        return self.name

    def __str__(self):
        """Retrieve string representation of the user"""
        return self.email

# Create your models here.
