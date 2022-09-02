from django.contrib import admin
from django.urls import path
from images import views

urlpatterns = [
    path('', views.get_img_url, name='images')
]
