from __future__ import absolute_import, unicode_literals
from email.mime import image
from celery import shared_task

from asyncio import sleep
from backend.celery import app
# import sys
# sys.path.append( "/backend/ai/photo_restoration/processAI")
from ai.photo_restoration.processAI import ai_process




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
def ai_task(request):
    image_url = 0
    # result = get_ai_result(image_url)

    #ai 처리
    # for i in range(999999):
    #     sleep(10)
    #     print("잠자는중")
    #     image_url = image_url+1
    ai_process("uuid","imgPath")
   
    return image_url

