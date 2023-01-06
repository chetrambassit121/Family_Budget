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

urlpatterns = [
    path("project/", ProjectAPIView.as_view(), name="project-api"),
    path("create-project/", ProjectCreateAPIView.as_view(), name="create"),
    path("expense/", ExpenseAPIView.as_view(), name="expense-api"),
    path("create-expense/", CreateExpenseAPIView.as_view(), name="expense-api"),
    path("category/", CategoryAPIView.as_view(), name="category-api"),
    path("create-category/", CategoryCreateAPIView.as_view(), name="category-create-api"),
]