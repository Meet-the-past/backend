from django.urls import path

from .views import View

urlpatterns = [
    path('v1/test/', View.as_view(), name='test'),
]