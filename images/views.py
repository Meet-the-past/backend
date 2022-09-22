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


'''
//향후 유틸로 분리하여 코드 활용하기 (특정 이미지를 받으면 버킷에 저장)
-> 매개변수로 파일이 저장된 위치를 받고 return으로 해당 이미지가 저장된 url
'''
@api_view(['POST']) 
def get_img_url(request):
    try:
        payload = user_token_to_data(request.headers.get('Authorization', None))
        print(payload)

        if(user.objects.filter(user_id=payload['id'])):

            image = request.FILES['origin_url']
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            image_type = "jpg"
            image_uuid = str(uuid.uuid4())
            s3_client.put_object(Body=image, Bucket='meet-the-past', Key=image_uuid + "." + image_type)
            image_url = "http://meet-the-past.s3.ap-northeast-2.amazonaws.com/" + \
                        image_uuid + "." + image_type
            image_url = image_url.replace(" ", "/")
            ##이미 존재하는 user_id에 orgin_url 과 status를 업데이트 하는 방식으로 해야되는가?
            
            
            Images.objects.create(origin_url = image_url, status = 'SUCCESS', user_id=user.objects.get(user_id=payload['id']))
            return Response(image_url)
            

        else:
            return Response("no vaild token")
                                #f'{image_url}'
                                #user_id = 1,##이부분 나중에 바꿔야 함
                                #status

            # image = images()
            # image.origin_url = image_url
            # image.save()
        return Response(False)
          

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)


'''
 @ fuction delete_images - history에 저장된 이미지 삭제
 @ param : imageId 
 
'''


@api_view(['DELETE'])
def delete_images(request, Id):
    payload = user_token_to_data(request.headers.get('Authorization', None))
    if (Images.objects.filter(user_id=payload.get('id'))):
        try:
            update = Images.objects.get(id=Id)
            update.is_deleted = True
            update.save()
            return Response(True)
        except Exception as ex:
            print(ex)
            return Response(False)
    # 유효한 토큰인지 확인하느 ㄴ코드추가
    


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


@api_view(['GET'])
def get_history(request):
    try:
        payload = user_token_to_data(request.headers.get('Authorization', None))

        if(user.objects.filter(user_id=payload['id'])):
            image= Images.objects.filter(user_id=payload.get('id'),is_deleted=False)
            serializer = PhotoSerializer(image, many=True)
            return JsonResponse({"data": serializer.data})

    except Exception as ex:
        print(ex)
        print("예외가 발생")
        return Response(False)
