from django.urls import path
from app import views

urlpatterns = [
    path('weChatLogin/', views.WeChatLogin.as_view()),
    path('weChatSignature/', views.WeChatSignature.as_view()),
    path('verifyLogin/', views.VerifyLogin.as_view()),
]
