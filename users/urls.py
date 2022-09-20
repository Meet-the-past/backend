from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.user_sign_up),
    path('email/validation/', views.user_is_duplicate),
    path('auth/', views.login),
    path('auth/reissue/', views.user_reissuance_access_token),
]