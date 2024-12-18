# accounts/serializers.py
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
class CustomRegisterSerializer(RegisterSerializer):
    # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
      required=True,
      allow_blank=True,
      max_length=255
    )

    # profileimage 필드를 추가
    profileimage = serializers.ImageField(
        allow_null=True,  # Null 값 허용
        required=False,   # 필수 값이 아니므로 False로 설정
    )

    # 해당 필드도 저장시 함께 사용하도록 설정합니다. 
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            # nickname 필드 추가
            'nickname': self.validated_data.get('nickname', ''),
            # 프로필 이미지 추가
            'profileimage': self.validated_data.get('profileimage', None),
        }

from django.contrib.auth import get_user_model
UserModel = get_user_model()
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')   
        if hasattr(UserModel, 'profileimage'):  # profileimage 필드 추가
            extra_fields.append('profileimage')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)