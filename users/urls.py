from django.contrib import admin
from django.urls import path
# from images import views
from . import views
from .views import create, user_list_create_api_view, hello_world

urlpatterns = [
    # path('', views.users.as_view(), name='users')
    path('create/', views.create.as_view()),
    path('user_list_create_api_view/', user_list_create_api_view),
    path('hello_world/', hello_world),
]
