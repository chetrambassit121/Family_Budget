from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)

from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from markdown_deux import markdown
from django.utils.safestring import mark_safe
# from family_budget.models import Project


# from family_budget.models import Project, Category, Expense
# from family_budget.models import Project




class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email")
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user_profile(self, user, pk):
        user_profile = self.model(user=user, pk=pk)
        user_profile.save(using=self._db)
        return user_profile

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), username=username, password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(verbose_name="date_joined", default=timezone.now)
    last_login = models.DateTimeField(verbose_name="last_login", default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = MyAccountManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_markdown(self):
        username = self.username
        markdown_text = markdown(username)
        return mark_safe(markdown_text)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    objects = MyAccountManager()

    # projects = models.ForeignKey(Project, null=True)

    def get_absolute_url(self):
        return reverse("home")

    def __str__(self):
        return str(self.user)

    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()