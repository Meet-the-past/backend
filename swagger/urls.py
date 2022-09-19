from django.urls import path
# from ..users import views
from .views import View, SerializerView

urlpatterns = [
    path('v1/test/', View.as_view(), name='test'),
    path('v1/serializer/', SerializerView.as_view(), name='serializer'),
    # path('v1/users/post', views.user_sign_up, name='user_sign_up'),
    # path('v1/users/login', views.login, name='login'),
    # path('v1/users/user_is_duplicate', views.user_is_duplicate, name='user_is_duplicate'),
    # path('v1/users/user_reissuance_access_token', views.user_reissuance_access_token, name='user_reissuance_access_token'),
]