import boto3 as boto3
from django.shortcuts import render

# from .models import BlogPost
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
import uuid
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from django.http import JsonResponse


class Images(APIView):  ##S
    def post(self, request, format=None):
        serializers = PhotoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_img_url(image):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    image_type = "jpg" or "png"
    image_uuid = str(uuid.uuid4())
    s3_client.put_object(Body=image, Bucket='mpt-bucket', Key=image_uuid + "." + image_type)
    image_url = "http://mpt-bucket.s3.ap-northeast-2.amazonaws.com/" + \
                image_uuid + "." + image_type
    image_url = image_url.replace(" ", "/")
    return image_url
