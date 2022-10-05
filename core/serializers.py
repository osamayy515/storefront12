from djoser.serializers import UserSerializer as BaseUserSerailizer, UserCreateSerializer as BaseUserCreateSerializer, TokenCreateSerializer as BaseTokenCreateSerializer
from rest_framework import serializers
from djoser.conf import settings
from django.contrib.auth import authenticate, get_user_model
from .models import User

# User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','password','email','first_name','last_name']

class UserSerializer(BaseUserSerailizer):

    class Meta(BaseUserSerailizer.Meta):
        fields = ['id','username','email','first_name','last_name']

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class CustomJWTSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         credentials = {
#             'username': '',
#             'password': attrs.get("password")
#         }

#         # This is answering the original question, but do whatever you need here. 
#         # For example in my case I had to check a different model that stores more user info
#         # But in the end, you should obtain the username to continue.
#         user_obj = User.objects.filter(email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()
#         if user_obj:
#             credentials['username'] = user_obj.username

#         return super().validate(credentials)

# class TokenCreateSerializer(BaseTokenCreateSerializer):
    
#     def __init__(self, *args, **kwargs):
#         super(TokenCreateSerializer, self).__init__(*args, **kwargs)
#         self.user = None
#         self.fields[settings.EMAIL_FIELD] = serializers.EmailField(required=False)

#     def validate(self, attrs):
#         self.user = authenticate(
#             email=attrs.get(settings.EMAIL_FIELD),
#             password=attrs.get('password'))

#         self._validate_user_exists(self.user)
#         self._validate_user_is_active(self.user)
#         return attrs

#     def _validate_user_exists(self, user):
#         if not user:
#             self.fail('invalid_credentials')

#     def _validate_user_is_active(self, user):
#         if not user.is_active:
#             self.fail('inactive_account')

# class TokenCreateSerializer(BaseTokenCreateSerializer):
    # password = serializers.CharField(required=False, style={"input_type": "password"})
# 
    # default_error_messages = {
        # "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        # "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
    # }
# 
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # self.user = None
# 
        # self.email_field = get_user_email_field_name(User)
        # self.fields[self.email_field] = serializers.EmailField()
# 
    # def validate(self, attrs):
        # password = attrs.get("password")
        # email = attrs.get("email")
        # self.user = authenticate(
            # request=self.context.get("request"), email=email, password=password
        # )
        # if not self.user:
            # self.user = User.objects.filter(email=email).first()
            # if self.user and not self.user.check_password(password):
                # self.fail("invalid_credentials")
        # if self.user and self.user.is_active:
            # return attrs
        # self.fail("invalid_credentials")