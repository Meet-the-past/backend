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

import io
from celery.result import AsyncResult

from users.models import user

from .models import *
from django.core import serializers
import json
from django.core.files.storage import default_storage

from .utils import *


# class Images(APIView):
#     def post(self, request, format=None):
#         serializers = PhotoSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


'''
//향후 유틸로 분리하여 코드 활용하기 (특정 이미지를 받으면 버킷에 저장)
-> 매개변수로 파일이 저장된 위치를 받고 return으로 해당 이미지가 저장된 url
'''
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
 @ ai_task.delay 함수에서 실제 AI코드 돌아감
'''
from .tasks import ai_task
@api_view(['POST'])
def get_task_id(request):


    uuidValue = str(uuid.uuid4()) #고유한 폴더명
    imageName = str(uuid.uuid4()) #고유한 이미지명

    file = request.FILES['filename'] 
    default_storage.save('ai_image/'+uuidValue+'/'+imageName+".png", file) #파일을 받아 저장

    image_url = uploadBucket('ai_image/'+uuidValue+'/'+imageName+'.png') #버킷 업로드
    #향후 이미지의 정확한 파일명 알아낼 것

    image = images()
    image.id = uuidValue
    image.origin_url = image_url
    image.save()
    print("테이블에 정상적으로 저장되었어요")


    #2. 이미지를 받아서 특정 경로에 원하는 이름으로 저장하기 (O)

    #3. 해당 경로로부터 이미지를 버킷에 올리고 Url받아오기 (O)

    #4 . url값 이미지 테이블에 저장하기 (O)

    #5.  task = ai_task.delay(uuid, filename)
    task = ai_task.delay("asd")
    return JsonResponse({"task_id": task.id})


'''
 @ fuction get_task_result - taskId값을 받아 AI결과의 처리여부 확인 및 결과 url 반환
 @ param : taskId 
 @ 추가해야할 부분 : userId의 경우 토큰을 통해 식별하기때문에 유저확인을 위한 코드부분은 수정해야합니다.
'''
@api_view(['GET'])
def get_task_result(request, user_id, task_id):
    task = AsyncResult(task_id)
    if not task.ready():  # 작업이 완료되지 않았을 경우
        return JsonResponse({"ai_result": "Wait a minute please"})


    #작업이 완료되면(즉 이미지가 생성되었다면) 값을 꺼내오기 (이미지를 지운다거나, 버킷에 올리거나 하는 일은 여기서 해선 안됨.
    # 여기서 해야하는 일은 반복해도 괜찮은 일)
    ai_results = task.get("ai_results")
    image_url = task.get("image_url")
    
    
    if image_url == 0:  # ai 결과가 없을 경우
        return JsonResponse({"ai_result": "false"})


    else :
        return JsonResponse({'image_id': image_url})

  


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
