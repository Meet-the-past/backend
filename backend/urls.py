"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include , re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="reBike APIs",
        default_version='v1',
        description="reBike 프로젝트 API 목록입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

from django.urls import path, include, re_path
from drf_yasg import openapi
from rest_framework import routers, permissions
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view

router = routers.DefaultRouter()


schema_view_patterns = [
    path('', include('users.urls'), name='users_api'),
    # path(r'^v1/', include('movie.urls', namespace='movie_api')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Meet The Past API",  # 타이틀
        default_version='v1',   # 버전
        description="AI service for old pics renewer",   # 설명
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_view_patterns,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/images/', include('images.urls'), name='images'),#s
    path('api/v1/users/', include('users.urls'), name='users'),
    # path('api/images', include('images.urls'), name='images'),#s
    path('api/users', include('users.urls'), name='users'),
    path('api/', include('swagger.urls'), name='api'),
   # 이 부분은 뭔지 몰라서 일단 주석처리 path('v1/api/users', include('users.urls'), name='users'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('api/images', include('images.urls'), name='images'),#s
#     # path('api/', include('swagger.urls'), name='api'),
#
# ]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]