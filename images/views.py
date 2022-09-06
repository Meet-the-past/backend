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


# from uilts import upload_file
# from datetime import datetime

# class Images(APIView):  ##S
#     def post(self, request, format=None):
#         serializers = PhotoSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



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

@api_view(['POST']) #추후 post로 바꿀 예정
def get_history(request):
    try:
        
        #토큰으로 받은 아이디
        image_id = request.POST['Id']#임시로 
        
        #update = images.objects.get(id=Id)
        # update.save()
        a="D"#Account.objects.filter(id= Id).only("origin_url", "converted_url")
        print(a)

        return Response(True)

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)