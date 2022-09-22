from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.urls import reverse
from requests import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .models import user
from .serializers import UserSerializer, CustomRegisterSerializer, UserSignupResponse

# 누구나 접근 가능 (회원가입 , 아이디 중복시 Error 반환하도록 설계 필요)
from .utils import *


# @permission_classes([AllowAny])
# class create(generics.GenericAPIView):
#     serializer_class = CustomRegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid(raise_exception=True):
#             return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
#         serializer.is_valid(raise_exception=True)
#
#         user = serializer.save()  # request 필요 -> 오류 발생 //
#         return HttpResponse(status=200)
#

# Singup
@api_view(['POST'])
def user_sign_up(request):
    name = request.data['name']
    password = request.data['password']
    email = request.data['email']

    new_user = user_create_client(name, email, password)
    data = UserSignupResponse(new_user, many=False).data
    return JsonResponse(data, status=201)


# Login
@api_view(['POST'])
def login(request):
    input_email = request.data['email']
    input_password = request.data['password']
    access_token = None
    refresh_token = None
    #비밀번호 예외처리
    if input_password and input_email:
        user_data = user_find_by_email(input_email).first()
        if user_data:
            access_token = user_generate_access_token(user_data)
            refresh_token = user_generate_refresh_token(user_data)
        else:
            return JsonResponse({"message": "invalid_data"}, status=400)

    data = {"accessToken": access_token, "refreshToken": refresh_token,
            "expiredTime": datetime.utcnow() + timedelta(minutes=30),
            "email": user_data.email}

    return JsonResponse({"result": data}, status=200)


# ID duplication check
@api_view(['POST'])
def user_is_duplicate(request):
    email = request.data['email']

    emailValidation = UserDuplicateCheck().email(email)

    if emailValidation:
        return JsonResponse({"message": "Duplicated email"}, status=401)
    return JsonResponse({"result": "New email"}, status=200)


# refreshtoken 재발급
@api_view(['POST'])
def user_reissuance_access_token(request):
    token = request.headers.get('Authorization', None)
    payload = user_token_to_data(token)

    if payload:
        # new access_token 반환
        if payload.get('type') == 'refresh_token':
            access_token = user_refresh_to_access(token)
            return JsonResponse({"accessToken": access_token,
                                 "expiredTime": datetime.utcnow() + timedelta(minutes=30)}, status=200)
        else:
            return JsonResponse({"message": "Not refresh_token"}, status=401)
    else:
        return JsonResponse({"message": payload}, status=401)
