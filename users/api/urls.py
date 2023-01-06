from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from .views import (
    UserLoginAPIView,
    UserCreateAPIView,
    UserListAPIView,
    UserProfileAPIView,
    LoginAPI
    # ProjectAPIView
)

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="login-api"),  
    path('logout/', knox_views.LogoutView.as_view(), name='logout-api'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path("login/", LoginAPI.as_view(), name="login-api"),  
    path("register/", UserCreateAPIView.as_view(), name="register-api"), 
    path("user-list/", UserListAPIView.as_view(), name="user-list-api"),
    path("user-profile/<int:id>/", UserProfileAPIView.as_view(), name="user-profile-api"),
    # path("project/", ProjectAPIView.as_view(), name="project-api")
]