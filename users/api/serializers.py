from asyncore import write
from users.views import profilepageview
from users.models import User, UserProfile
# from .views import UserProfileAPIView
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.serializers import (  # charfield
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from rest_framework import serializers
from family_budget.api.serializers import ProjectSerializer
from family_budget.models import Project, Category, Expense
# from family_budget.api.serializers import ProjectSerializer

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "token"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data["password"]
        if not username:
            raise ValidationError("Username required to login")

        user = User.objects.filter(Q(username=username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials")

        data["token"] = "SOME RANDOM TOKEN"

        return data

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    username = CharField(label="Username")
    password = CharField(write_only=True)
    password2 = CharField(label="Re-enter Password", write_only=True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]


    def validate(self, data):
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("User already exists")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get("password")
        password2 = value
        if password != password2:
            raise ValidationError("Passwords must match")
        return value

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


# class UserProjectSerializer(ModelSerializer):
class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
    

class UserProfileSerializer(ModelSerializer):
    # profile = UserProfile.objects.get(pk=pk)
    user = UserDetailSerializer()
    # p = Project.objects.filter(author=user)
    # projects = ProjectSerializer()
    
    class Meta:
        model = UserProfile
        fields = [
            # "id",
            "user",
            # "username"
            # "projects"
            # pro
        ]
    # def profileview(request, pk, *args, **kwargs):
    #     if request.method == 'GET':
    #         profile = UserProfile.objects.get(pk=pk)
    #         user = profile.user
    #         projects = Project.objects.filter(author=user)
    #         return projects
   
# class UserDetailSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "date_joined"
#         ]
   

user_profile_url = HyperlinkedIdentityField(view_name='user-profile', lookup_field="pk")
class UserListSerializer(serializers.HyperlinkedModelSerializer, ModelSerializer):
    url = user_profile_url
    user = User.objects.all()
    html = SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "url",
            "pk",
            "username",
            "html"
        ]

    def get_html(self, obj):
        return obj.get_markdown()


