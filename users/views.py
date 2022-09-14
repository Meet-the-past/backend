from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from requests import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import user
from .serializers import UserSerializer, CustomRegisterSerializer



# 누구나 접근 가능 (회원가입 , 아이디 중복시 Error 반환하도록 설계 필요)
@permission_classes([AllowAny])
class create(generics.GenericAPIView):
    serializer_class = CustomRegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.is_valid(raise_exception=True)

        user = serializer.save() # request 필요 -> 오류 발생 //
        return HttpResponse(status=200)

   



