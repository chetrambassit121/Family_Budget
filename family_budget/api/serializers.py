from users.models import User, UserProfile
# from users.api.serializers import UserListSerializer
from family_budget.models import Project, Category, Expense
from rest_framework.serializers import (  
    ModelSerializer,
)


class ProjectSerializer(ModelSerializer):
    # author = UserListSerializer()
    class Meta:
        model = Project
        fields= [
            "name",
            "budget",
            "slug",
            # "author"
        ]





class CategorySerializer(ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = Category
        fields = [
            "project",
            "name"
        ]



class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "project",
            "name"
        ]

class ProjectCreateSerializer(ModelSerializer):
    # author = UserListSerializer()
    # category = CategorySerializer()

    class Meta:
        model = Project
        fields= [
            "name",
            "budget",
            # "author"
            # "category"
        ]


class ExpenseSerializer(ModelSerializer):
    project = ProjectSerializer()
    category = CategorySerializer()
    class Meta:
        model = Expense
        fields = [
            "project",
            "title",
            "amount",
            "category"
        ]

class CreateExpenseSerializer(ModelSerializer):
    # project = ProjectSerializer()
    # category = CategorySerializer()
    class Meta:
        model = Expense
        fields = [
            "project",
            "title",
            "amount",
            "category"
        ]
