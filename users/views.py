from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from .serializers import UserSignupResponse, CustomRegisterSerializer, AccountLoginSerializer, \
    CheckDuplicationSerializer

# 누구나 접근 가능 (회원가입 , 아이디 중복시 Error 반환하도록 설계 필요)
from .utils import *

# Singup
@swagger_auto_schema(
    method='post',
    operation_summary='''사용자 회원가입''',
    request_body=CustomRegisterSerializer,
    responses={
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema('사용자 이름', type=openapi.TYPE_STRING),
                'email': openapi.Schema('사용자 이메일', type=openapi.TYPE_STRING),
                'password': openapi.Schema('사용자 패스워드', type=openapi.TYPE_STRING),
        }
    )}
)
@api_view(['POST'])
def user_sign_up(request):
    name = request.data['name']
    email = request.data['email']
    password = request.data['password']

    new_user = user_create_client(name, email, password)
    data = UserSignupResponse(new_user, many=False).data
    return JsonResponse(data, status=201)


# Login
@swagger_auto_schema(
    method='post',
    operation_summary='''사용자 로그인''',
    request_body=AccountLoginSerializer,
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'accessToken': openapi.Schema('access token', type=openapi.TYPE_STRING),
                'refreshToken': openapi.Schema('refresh token', type=openapi.TYPE_STRING),
                'expiredTime': openapi.Schema('expired time', type=openapi.TYPE_NUMBER), # 타입이 맞나...?
                'email': openapi.Schema('사용자 이메일', type=openapi.TYPE_STRING),
            }
        )}
)
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


@swagger_auto_schema(
    method='post',
    operation_summary='''ID duplication check''',
    request_body=CheckDuplicationSerializer,
    responses={200: 'You can use this email'}
)
@api_view(['POST'])
def user_is_duplicate(request):
    email = request.data['email']
    emailValidation = UserDuplicateCheck().email(email)

    if emailValidation:
        return JsonResponse({"message": "Duplicated email"}, status=401)
    return JsonResponse({"result": "New email"}, status=200)


@swagger_auto_schema(
    method='post',
    operation_summary='''refreshtoken 재발급''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema('사용자 token', type=openapi.TYPE_STRING),
        },
        required=['token']  # 필수값을 지정 할 Schema를 입력해주면 된다.
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema('access_token', type=openapi.TYPE_STRING),
                'expiredTime': openapi.Schema('expiredTime', type=openapi.TYPE_STRING),
            }
        ),
        401: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema('Not refresh_token', type=openapi.TYPE_STRING),
            }
        )
    }
)
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
