from __future__ import absolute_import, unicode_literals
from celery import shared_task

from asyncio import sleep


from backend.celery import app



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
    image_url = "향후 함수 추가 필요"
    # result = get_ai_result(image_url)
    sleep(10)
    #ai 처리
    return image_url

