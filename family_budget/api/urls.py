from django.contrib import admin
from django.urls import path, include

from .views import (
    ProjectAPIView,
    ExpenseAPIView,
    CreateExpenseAPIView,
    CategoryAPIView,
    ProjectCreateAPIView,
    CategoryCreateAPIView
)
from . import views
from rest_framework.routers import DefaultRouter
from users.api.urls import router as users_router
from patches import routers
router = routers.DefaultRouter()
router.extend(users_router)
router.register(r'project', views.ProjectAPIView, basename="project")
router.register(r'create-project', views.ProjectCreateAPIView, basename="create-project")
router.register(r'expense', views.ExpenseAPIView, basename="expense")
router.register(r'create-expense', views.CreateExpenseAPIView, basename="create-expense")
router.register(r'category', views.CategoryAPIView, basename="category")
router.register(r'create-category', views.CategoryCreateAPIView, basename="create-category")
# router.register(r'user-list', views.UserListAPIView, basename="user-list")
# router.register(r'user-profile', views.UserProfileAPIView)

urlpatterns = [
    path('api/', include(router.urls), name="api-root"),
    path("project/", ProjectAPIView.as_view({'get': 'list'}), name="project-api"),
    path("create-project/", ProjectCreateAPIView.as_view({'get': 'list'}), name="create"),
    path("expense/", ExpenseAPIView.as_view({'get': 'list'}), name="expense-api"),
    path("create-expense/", CreateExpenseAPIView.as_view({'get': 'list'}), name="expense-api"),
    path("category/", CategoryAPIView.as_view({'get': 'list'}), name="category-api"),
    path("create-category/", CategoryCreateAPIView.as_view({'get': 'list'}), name="category-create-api"),
]

# urlpatterns = [
#     path('', include(router.urls)),
# ]

