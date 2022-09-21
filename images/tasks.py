from __future__ import absolute_import, unicode_literals
from email.mime import image
from .models import images
from celery import shared_task

from asyncio import sleep
from backend.celery import app
# import sys
# sys.path.append( "/backend/ai/photo_restoration/processAI")
from ai.photo_restoration.processAI import ai_process
from .utils import uploadBucket





@app.task
def add(x, y):
    sleep(50)
    return x + y


# @app.task
# def ai_task(request):
#     # result = get_ai_result(request)
#     image_url = get_img_url(request)
#
#     if result["ai_results"] == 0:
#         return {"ai_results": 0, "image_url": 0}
#     return {"ai_results": result["ai_results"], "image_url": image_url}

#from .views import get_img_url
@app.task
def ai_task(path, name):
    status = False
    # result = get_ai_result(image_url)

    #ai 처리
    # for i in range(999999):
    #     sleep(10)
    #     print("잠자는중")
    #     image_url = image_url+1
    ai_process(path,name)
    after_url = uploadBucket('ai_image/'+path+'/final_output'+name+'.png') #버킷 업로드
    print("결과를 버킷에 업로드합니다.")
    
    try:
        update = images.objects.get(id=path)
        update.converted_url = after_url
        update.save()
        print("업데이트 성공")
        
    except Exception as ex:
        print(ex)
        
    status = True
    
    #처리가 끝났으면 이미지를 버킷에 올리고, db에 저장하는 작업을 진행해야함. 이후 완료를 알리는 값을 반환하면 끝
    # 1. 버킷에 올리기 - 처리된 결과 이미지의 저장경로를 알아야한다. 경로만 알아도된다면 이미지명은 상관없음 , 단 이미지 이름도 알아야한다면 애초에 저장할 때 이미지명을 지정해서 저장하고 
    # 그 이미지 str을 넘겨줘야한다. 

    # 버킷 url값을 가져왔으면 db에 값을 저장하기
    return status

