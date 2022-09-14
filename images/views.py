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
