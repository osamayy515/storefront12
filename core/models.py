from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager
from django.db.models import Q

# class CustomUserManager(UserManager):

#     def get_by_natural_key(self, username):
#         return self.get(
#             Q(**{self.model.USERNAME_FIELD: username}) |
#             Q(**{self.model.EMAIL_FIELD: username})
#         )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # objects = CustomUserManager()

# from django.contrib.auth.models import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.db import models
# 
# 
# Create your models here.
# class UserManager(BaseUserManager):
    # def create_user(self, email,  password=None, **kwargs):
        # if not email:
            # raise ValueError("Users must have an email address")
        # email = self.normalize_email(email)
        # user = self.model(email=email, **kwargs)
        # user.set_password(password)
        # user.save()
        # return user
    # def create_superuser(self, email,  password=None, **kwargs):
        # kwargs.setdefault('is_active', True)
        # kwargs.setdefault('is_staff', True)
        # kwargs.setdefault('is_superuser', True)
        # if kwargs.get('is_active') is not True:
            # raise ValueError('Superuser must be active')
        # if kwargs.get('is_staff') is not True:
            # raise ValueError('Superuser must be staff')
        # if kwargs.get('is_superuser') is not True:
            # raise ValueError('Superuser must have is_superuser=True')
        # return self.create_user(email, password, **kwargs)
# 
# class User(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255, unique=True)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # is_active = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
# 
    # objects = UserManager()
# 
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']
# 
    # def get_full_name(self):
        # return f"{self.first_name}{self.last_name}"
# 
    # def get_short_name(self):
        # return self.first_name
# 
    # def __str__(self):
        # return self.email
# 