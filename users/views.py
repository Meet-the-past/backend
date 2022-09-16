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
from .serializers import UserSerializer, CustomRegisterSerializer

# 누구나 접근 가능 (회원가입 , 아이디 중복시 Error 반환하도록 설계 필요)
from .utils import user_find_by_name, user_comppassword, user_generate_access_token, user_generate_refresh_token, \
    user_find_by_email


@permission_classes([AllowAny])
class create(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # request 필요 -> 오류 발생 //
        return HttpResponse(status=200)


# Login
def login(request):
    input_email = request.data['email']
    input_password = request.data['password']
    access_token = None
    refresh_token = None

    if input_password and input_email:
        user_data = user_find_by_email(input_email).first()
        if user_data:
            if user_comppassword(input_password, user_data):
                access_token = user_generate_access_token(user_data)
                refresh_token = user_generate_refresh_token(user_data)
        else:
            return JsonResponse({"message": "invalid_data"}, status=400)

    data = {"access_token": access_token, "refresh_token": refresh_token,
            "expiredTime": datetime.utcnow() + timedelta(minutes=30),
            "email": user_data.email}

    return JsonResponse({"result": data}, status=200)
