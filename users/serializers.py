from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework_jwt.settings import api_settings

from .models import user

# JWT 사용을 위한 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# User = get_user_model()

# 회원가입
class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['email', 'name', 'password']


# 회원가입
class CustomRegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)
    email = serializers.CharField(required=False, max_length=128)
    password = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = user
        fields = ['email', 'name', 'password']

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data() # username, password, email이 디폴트
        data_dict['name'] = self.validated_data.get('name', '')
        data_dict['email'] = self.validated_data.get('email', '')
        data_dict['password'] = self.validated_data.get('password', '')

        return data_dict



# 로그인
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=30)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         username = data.get("username")
#         password = data.get("password", None)
#         # 사용자 아이디와 비밀번호로 로그인 구현(<-> 사용자 아이디 대신 이메일로도 가능)
#         user = authenticate(username=username, password=password)
#
#         if user is None:
#             return {'username': 'None'}
#         try:
#             payload = JWT_PAYLOAD_HANDLER(user)
#             jwt_token = JWT_ENCODE_HANDLER(payload)
#             update_last_login(None, user)
#
#         except User.DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with given username and password does not exist'
#             )
#         return {
#             'username': user.username,
#             'token': jwt_token
#         }

# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('email', 'name')
#

# class UserSerializer(serializers.ModelSerializer) :
#     class Meta :
#         model = user        # user 모델 사용
#         fields = '__all__'            # 모든 필드 포함