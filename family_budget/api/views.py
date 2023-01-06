from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response  
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST  
from rest_framework.views import APIView  
from users.models import User, UserProfile
from family_budget.models import Project, Expense, Category
from .serializers import (
    ProjectSerializer,
    ProjectCreateSerializer,
    ExpenseSerializer,
    CategorySerializer,
    CreateExpenseSerializer
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from .pagination import ProjectLimitOffsetPagination, ProjectPageNumberPagination


class ProjectAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProjectPageNumberPagination


class ExpenseAPIView(ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateExpenseAPIView(CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = CreateExpenseSerializer
    permission_classes = [AllowAny]

class CategoryAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def post(self, request, *args, **kwargs):
        form = ProjectSerializer(request.POST, request.FILES)
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.author = request.user
            new_project.save(request)
            categories = self.request.POST['categoriesString'].split(',')
            for category in categories:
                Category.objects.create(
                    project=Project.objects.get(id=new_project.id),
                    name=category
                ).save()
            form = ProjectSerializer()

        