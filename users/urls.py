from django.urls import path
# from images import views
from . import views


urlpatterns = [
    # path('', views.users.as_view(), name='users')
    # path('create/', views.create.as_view()),
    path('create/', views.user_sign_up),
    path('email/validation/', views.user_is_duplicate),
    path('auth/', views.login),
    path('auth/reissue/', views.user_reissuance_access_token),
]