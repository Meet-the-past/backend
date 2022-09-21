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
from drf_yasg.views import get_schema_view

router = routers.DefaultRouter()
schema_url_patterns = [
    path('api/v1/users/', include('users.urls')),
    path('api/v1/images/', include('images.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Meet The Past API",  # 타이틀
        default_version='v1',   # 버전
        description="AI service for old pics renewer",   # 설명
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/images/', include('images.urls'), name='images'),#s
    path('api/v1/users/', include('users.urls'), name='users'),
    # path('api/images', include('images.urls'), name='images'),#s
    path('api/users', include('users.urls'), name='users'),
    path('api/', include('swagger.urls'), name='api'),

    # # Auto DRF API docs
    # path(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path(r'^swagger/v1/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path(r'^redoc/v1/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
