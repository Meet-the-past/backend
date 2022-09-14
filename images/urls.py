from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_task_id, name='images')
]
