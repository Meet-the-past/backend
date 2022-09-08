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
from rest_framework.decorators import api_view
from .models import *
from django.core import serializers
import json

@api_view(['POST'])
def get_img_url(request):
    try:
        
        image = request.FILES['origin_url']
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        image_type = "jpg" or "png"
        image_uuid = str(uuid.uuid4())
        s3_client.put_object(Body=image, Bucket='meet-the-past', Key=image_uuid + "." + image_type)
        image_url = "http://meet-the-past.s3.ap-northeast-2.amazonaws.com/" + \
                    image_uuid + "." + image_type
        image_url = image_url.replace(" ", "/")
        print(image_url)
        images.objects.create(origin_url = image_url,status = 'SUCCESS')
                            #f'{image_url}'
                            #user_id = 1,##이부분 나중에 바꿔야 함
                            #status

        # image = images()
        # image.origin_url = image_url
        # image.save()
            
        return Response(True)

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)

@api_view(['DELETE'])
def delet_images(request,Id):
    try:
        update = images.objects.get(id=Id)
        update.is_deleted = True
        update.save()
        return Response(True)

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)

###test코드
@api_view(['POST'])
def get_history(request):
    try:
        
        #토큰으로 받은 아이디
        user_id = request.POST['user_id']#임시로 

        image=images.objects.filter(status = "SUCCESS",is_deleted=False)
        serializer=imagesSerializer(image, many=True)
        
        return Response(serializer.data)
       
    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)


#실제 코드 
# @api_view(['GET'])
# def get_history(request):
#     try:
        
#         #토큰으로 받은 아이디
       

#         image=images.objects.filter(user_id = "token으로 받은 값")
#         serializer=imagesSerializer(image, many=True)
#         return Response(serializer.data)
       
#     except Exception as ex:
#         print(ex)
#         print("예외가 발생")
#         return Response(False)

