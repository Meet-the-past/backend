from email.mime import image
from PIL import Image
from django.core.cache import cache
from .models import images
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
import uuid
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from django.http import JsonResponse
from rest_framework.decorators import api_view

from celery.result import AsyncResult

from users.models import user

from .models import *
from django.core import serializers
import json
from django.core.files.storage import default_storage

from .utils import *




# @api_view(['POST']) 
# def get_img_url(request):
#     try:

#         image = request.FILES['origin_url']
#         s3_client = boto3.client(
#             's3',
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#         )
#         image_type = "jpg"
#         image_uuid = str(uuid.uuid4())
#         s3_client.put_object(Body=image, Bucket='meet-the-past', Key=image_uuid + "." + image_type)
#         image_url = "http://meet-the-past.s3.ap-northeast-2.amazonaws.com/" + \
#                     image_uuid + "." + image_type
#         image_url = image_url.replace(" ", "/")
#         print(image_url)
#         Images.objects.create(origin_url = image_url,status = 'SUCCESS')
#                             #f'{image_url}'
#                             #user_id = 1,##이부분 나중에 바꿔야 함
#                             #status

#         # image = images()
#         # image.origin_url = image_url
#         # image.save()

#         return Response(True)

#     except Exception as ex:
#         print(ex)
#         print("예외가 발생")
#         return Response(False)


'''
 @ fuction delete_images - history에 저장된 이미지 삭제
 @ param : imageId 
 
'''


@api_view(['DELETE'])
def delete_images(request, Id):
    try:
        update = image.objects.get(id=Id)
        update.is_deleted = True
        update.save()
        return Response(True)
    except Exception as ex:
        print(ex)
        return Response(False)


'''
 @ fuction get_task_id - 사용자가 이미지를 업로드하면 taskID반환
 @ param : FormData("filename") 
 @ update-date : 2022-09-22
'''
from .tasks import ai_task

@api_view(['POST'])
def get_task_id(request):

    uuidKey = str(uuid.uuid4()) #고유한 폴더명
    imageName = str(uuid.uuid4()) #고유한 이미지명

    file = request.FILES['filename'] 
    default_storage.save('ai_image/'+uuidKey+'/'+imageName+".png", file) #파일을 받아 저장

    image_url = uploadBucket('ai_image/'+uuidKey+'/'+imageName+'.png') #버킷 업로드
  

    image = images()
    image.id = uuidKey
    image.origin_url = image_url
    image.save()
 
    task = ai_task.delay(uuidKey,imageName)
    return JsonResponse({"task_id": task.id})


'''
 @ fuction get_task_result - taskId값을 받아 AI결과의 처리여부 확인 및 결과 url 반환
 @ param : taskId 
 @ update-date : 2022-09-22
'''
@api_view(['GET'])
def get_task_result(request, task_id):
    task = AsyncResult(task_id)
    if not task.ready():  # 작업이 완료되지 않았을 경우
        return JsonResponse({"data": "RUNNING"})

    uuidKey = task.get()['uuid']
    image = images.objects.get(id=uuidKey)
    serializer = PhotoResultSerializer(image)
    return JsonResponse({"data": serializer.data})

'''
 @ fuction get_history - 사용자가 업로드한 이미지들을 반환
 @ ai_task.delay 함수에서 실제 AI코드 돌아감
 @향후 로그인 기능이 구현되면 헤더에서 받은 토큰을 이용해서 userId값 받을 것(실제 코드 부분 참고)

'''


@api_view(['POST'])
def get_history(request):
    try:
        # 토큰으로 받은 아이디
        user_id = request.POST['user_id']  # 임시로

        image = images.objects.filter(status="SUCCESS", is_deleted=False)
        serializer = PhotoSerializer(image, many=True)

        return JsonResponse({"data": serializer.data})

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)

# 실제 코드
# @api_view(['GET'])
# def get_history(request):
#     try:

#         #토큰으로 받은 아이디

#         image=images.objects.filter(user_id = "token으로 받은 값" ,is_deleted=False)
#         serializer=imagesSerializer(image, many=True)
#         return Response(serializer.data)

#     except Exception as ex:
#         print(ex)
#         print("예외가 발생")
#         return Response(False)
