from django.db import models

from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    # overriding the create_user() from BaseUserManager() class
    def create_user(self, email, password=None, **extra_fields):
        # extra_fields means take in any extra parameters that are passed
        """creates and saves a new user"""
        if not email:
            raise ValueError('Email address is required')
        user = self.model(email=self.normalize_email(email), **extra_fields) 
        # same as creating user model
        # normalize_email() is a helper function in BaseUserManager
        user.set_password(password) # using set_password() form BaseUSerManager to encrypt password
        user.save(using=self._db) # saving the user and self._db is used for supporting multiple databases

        return user
    
    def create_superuser(self,email, password):
        """ creates and saves a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True # all that required for creating a superuser
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() # creates a new userManager 

    USERNAME_FIELD = 'email' # override the default username fiels to email


