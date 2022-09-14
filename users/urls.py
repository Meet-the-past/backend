from django.urls import path
# from images import views
from . import views


urlpatterns = [
    # path('', views.users.as_view(), name='users')
    path('create/', views.create.as_view()),
]
