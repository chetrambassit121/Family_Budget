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
from family_budget.models import Project
from .serializers import (
    UserLoginSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserProfileSerializer,
    # ProjectSerializer
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
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Q
from .pagination import ProjectLimitOffsetPagination, ProjectPageNumberPagination




class LoginAPI(KnoxLoginView):
    permission_classes = (AllowAny)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



class UserLoginAPIView(KnoxLoginView):  
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):  
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserCreateAPIView(
    CreateAPIView
):  
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]



class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]



# class UserProfileAPIView(ListAPIView):
#     serializer_class = UserProfileSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     permission_classes = [IsAuthenticated]
#     search_fields = ['username','author']
#     def get_queryset(self, *args, **kwargs):
#         queryset_list = UserProfile.objects.all()
#         query = self.request.GET.get("q")
#         if query:
#             queryset_list = queryset_list.filter(
#                 Q(username__icontains=query)
#                 |
#                 Q(author__icontains=query)
#             ).distinct()
#         return queryset_list

class UserProfileAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    pagination_class = ProjectPageNumberPagination


    # def get(request, pk, *args, **kwargs):
    #     serializer = UserProfileSerializer(projects=projects)
    #     profile = UserProfile.objects.get(pk=pk)
    #     user = profile.user
    #     projects = Project.objects.filter(author=user)
            


# def profilepageview(request, pk, *args, **kwargs):
#     if request.method == 'GET':
#         profile = UserProfile.objects.get(pk=pk)
#         user = profile.user
#         p = Paginator(Project.objects.filter(author=user), 2)
#         page = request.GET.get("page")
#         projects = p.get_page(page)

    # def get(self, request, *args, **kwargs):

# profile = UserProfile.objects.get(pk=pk)
#         user = profile.user
#         p = Paginator(Project.objects.filter(author=user), 2)
#         page = request.GET.get("page")
#         projects = p.get_page(page)