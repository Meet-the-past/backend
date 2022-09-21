from __future__ import absolute_import, unicode_literals
from email.mime import image
from .models import images
from celery import shared_task

from backend.celery import app

from ai.photo_restoration.processAI import ai_process
from .utils import uploadBucket, deleteImage


@app.task
def ai_task(path, name):
   
    ai_process(path,name)
    after_url = uploadBucket('ai_image/'+path+'/final_output/'+name+'.png') #버킷 업로드
    print("결과를 버킷에 업로드합니다.")
    
    try:
        update = images.objects.get(id=path)
        update.converted_url = after_url
        update.save()
        print("업데이트 성공")
        
    except Exception as ex:
        print(ex)
    
    deleteImage('ai_image/'+path)

    return {"uuid" :path}

