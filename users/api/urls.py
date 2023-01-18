# from django.contrib import admin
# from django.urls import path, include 
# from .views import api_root

# urlpatterns = [
#     path('check-api-root/', api_root, name='api-root'),
#     path('', include('djoser.urls')),                    # 
#     path('', include('djoser.urls.authtoken')),
#     # path('auth/', api_root, name='api-root'),
    
# ]
































# from django.contrib import admin
# from django.urls import path, include
# from knox import views as knox_views
# from .views import (
#     UserLoginAPIView,
#     UserCreateAPIView,
#     UserListAPIView,
#     UserProfileAPIView,
#     # LoginAPI
#     # ProjectAPIView
# )
# from . import views

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'login', views.UserLoginAPIView.as_view(), basename="login")
# router.register(r'logout', knox_views.LogoutView.as_view(), basename="logout")
# # router.register(r'logoutall', knox_views.LogoutAllView.as_view(), basename="logoutall")
# router.register(r'register', views.UserCreateAPIView.as_view(), basename="register")
# router.register(r'user-list', views.UserListAPIView.as_view(), basename="user-list")
# router.register(r'user-profile/<int:id>/', views.UserProfileAPIView.as_view(), basename="user-profile")


# urlpatterns = [
#     path('', include(router.urls)),
# ]








































from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from .views import (
    UserLoginAPIView,
    UserCreateAPIView,
    UserListAPIView,
    UserProfileAPIView,
    # LoginAPI
    # ProjectAPIView
)
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'login', views.UserLoginAPIView, basename="login")
router.register(r'register', views.UserCreateAPIView, basename="register")
router.register(r'user-list', views.UserListAPIView, basename="user-list")
router.register(r'user-profile', views.UserProfileAPIView)

urlpatterns = [
    path('api/', include(router.urls), name="api-root"),
    path("login/", UserLoginAPIView.as_view({'get': 'list'}), name="login-api"),  
    path('logout/', knox_views.LogoutView.as_view(), name='logout-api'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path("login/", LoginAPI.as_view(), name="login-api"),  
    path("register/", UserCreateAPIView.as_view({'get': 'list'}), name="register-api"), 
    path("user-list/", UserListAPIView.as_view({'get': 'list'}), name="user-list-api"),
    path("user-profile/<int:id>/", UserProfileAPIView.as_view({'get': 'list'}), name="user-profile-api"),
    # path("project/", ProjectAPIView.as_view(), name="project-api")
]

# urlpatterns += [
#     path('api/', include(router.urls), name="api-root"),
# ]