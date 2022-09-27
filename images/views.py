from email.mime import image
from urllib import request
from PIL import Image
from django.core.cache import cache
from .models import images
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
from users.utils import *
from .utils import *
from backend.custom_exceptions import *
from rest_framework import exceptions

 


'''
 @ fuction delete_images - history에 저장된 이미지 삭제
 @ param : imageId 
 
'''

@swagger_auto_schema(
    method='delete',
    operation_summary='''이미지 삭제''',
)
@api_view(['DELETE'])
def delete_images(request, Id):
        try:
            payload = user_token_to_data(request.headers.get('Authorization', None))
            if (images.objects.filter(user_id=payload.get('id'))):
                    #update = get_object_or_404(images,id=Id)
                    update = images.objects.get(id=Id)
                    update.is_deleted = True
                    update.save()
                    return Response(True)

        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
            raise ValidationError()

        except Exception as ex:
            print(ex)
    
        
        # 유효한 토큰인지 확인하느 ㄴ코드추가
    

'''
 @ fuction get_task_id - 사용자가 이미지를 업로드하면 taskID반환
 @ param : FormData("filename") 
 @ update-date : 2022-09-22
'''

from .tasks import ai_task
@swagger_auto_schema(
    method='post',
    operation_summary='''이미지 업로드''',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema('사용자 token', type=openapi.TYPE_STRING),
            'filename' : openapi.Schema('이미지', type=openapi.IN_FORM),
        },
        required=['token']  # 필수값을 지정 할 Schema를 입력해주면 된다.
    ),
    responses={200: TaskIdSerializer}
)
@api_view(['POST'])
def get_task_id(request):

    try:
        payload = user_token_to_data(request.headers.get('Authorization', None))
        
        if(user.objects.filter(user_id=payload['id'])):
    
            uuidKey = str(uuid.uuid4()) #고유한 폴더명
            imageName = str(uuid.uuid4()) #고유한 이미지명

            file = request.FILES['filename'] 
            default_storage.save('ai_image/'+uuidKey+'/'+imageName+".png", file) #파일을 받아 저장

            image_url = uploadBucket('ai_image/'+uuidKey+'/'+imageName+'.png') #버킷 업로드
        

            image = images()
            image.id = uuidKey
            image.user_id=user.objects.get(user_id=payload['id'])
            image.origin_url = image_url
            image.status = 'SUCCESS'
            image.save()
        
            task = ai_task.delay(uuidKey,imageName)
            return JsonResponse({"task_id": task.id})
         

        return JsonResponse({"data": "error"})

    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
         raise ValidationError()

    except Exception as ex:
        print(ex)
        


'''
 @ fuction get_task_result - taskId값을 받아 AI결과의 처리여부 확인 및 결과 url 반환
 @ param : taskId 
 @ update-date : 2022-09-22
'''
@swagger_auto_schema(
    method='get',
    operation_summary='''처리된 AI결과 받아오기''',
    responses={200: PhotoResultSerializer}
)
@api_view(['GET'])
def get_task_result(request, task_id):
    try:
        payload = user_token_to_data(request.headers.get('Authorization', None))
        if(user.objects.filter(user_id=payload['id'])):
            task = AsyncResult(task_id)
            if not task.ready():  # 작업이 완료되지 않았을 경우
                return JsonResponse({"data": "RUNNING"})

            uuidKey = task.get()['uuid']
            image = images.objects.get(id=uuidKey)
            serializer = PhotoResultSerializer(image)
            return JsonResponse({"data": serializer.data})
        return JsonResponse({"data": serializer.data})

    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
         raise ValidationError()

    except Exception as ex:
        print(ex)
'''
 @ fuction get_history - 사용자가 업로드한 이미지들을 반환
 @ ai_task.delay 함수에서 실제 AI코드 돌아감
 @향후 로그인 기능이 구현되면 헤더에서 받은 토큰을 이용해서 userId값 받을 것(실제 코드 부분 참고)

'''
@swagger_auto_schema(
    method='get',
    operation_summary='''이미지 히스토리''',
    responses={200: 'get history result successfully'}
)

@api_view(['GET'])
def get_history(request):
    try:
    
        payload = user_token_to_data(request.headers.get('Authorization', None))
        
        if(user.objects.filter(user_id=payload['id'])):
           
            image= images.objects.filter(user_id=payload.get('id'),is_deleted=False)   
            serializer = PhotoSerializer(image, many=True)
            return JsonResponse({"data": serializer.data})

    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
         raise ValidationError()

    except Exception as ex:
        print(ex)
     