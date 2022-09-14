import boto3 as boto3
from PIL import Image
from django.core.cache import cache
from .models import Images
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
import uuid
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from django.http import JsonResponse
from rest_framework.decorators import api_view

import io
from celery.result import AsyncResult

from users.models import user

class Images(APIView):
    def post(self, request, format=None):
        serializers = PhotoSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
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

# url 받는 함수(sleep(50)) -> celery, 나중에 함수만 바꾸기.

# @api_view(['POST'])
def get_img_url(image):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    image_type = "jpg"
    image_uuid = str(uuid.uuid4())
    s3_client.put_object(Body=image, Bucket='mpt-bucket', Key=image_uuid + "." + image_type)
    image_url = "http://mpt-bucket.s3.ap-northeast-2.amazonaws.com/" + \
                image_uuid + "." + image_type
    image_url = image_url.replace(" ", "/")
    return image_url

from .tasks import ai_task
@api_view(['POST'])
def get_task_id(request):
    image = Image.open(io.BytesIO(request.FILES.get('filename').read()))

    img_instance = {
        'pixels': image.tobytes(),
        'size': image.size,
        'mode': image.mode,
    }
    task = ai_task.delay(img_instance)
    return JsonResponse({"task_id": task.id})

@api_view(['GET'])
def get_task_result(request, user_id, task_id):
    task = AsyncResult(task_id)
    if not task.ready():  # 작업이 완료되지 않았을 경우
        return JsonResponse({"ai_result": "Wait a minute please"})

    ai_results = task.get("ai_results")
    image_url = task.get("image_url")

    if ai_results['ai_results'] == 0:  # ai 결과가 없을 경우
        return JsonResponse({"ai_result": "false"})

    try:
        Images.objects.get(image=image_url["image_url"])
        return JsonResponse({"ai_result": "exist"})
    except Images.DoesNotExist:
        user_info = user.objects.get(id=user_id)
        Images.objects.create(
            image=image_url["image_url"], user_id=user_info)

        image_info = Images.objects.get(
            image=image_url["image_url"], user_id=user_info)

        return JsonResponse({'image_id': image_info.id})
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

