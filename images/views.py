from django.shortcuts import render

# from .models import BlogPost
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class Images(APIView):  ##S
    def post(self, request, format=None):
        serializers = PhotoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
