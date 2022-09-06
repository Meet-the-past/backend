from django.urls import path

from .views import View, SerializerView

urlpatterns = [
    path('v1/test/', View.as_view(), name='test'),
    path('v1/serializer/', SerializerView.as_view(), name='serializer'),
]