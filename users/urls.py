from django.urls import path
from . import views
# from .views import profilepageview, User_List, UserSearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LoginView



urlpatterns = [
      path('register', views.RegistrationView.as_view(), name='register'),
      path('login', views.LoginView.as_view(), name='login'),
      # path('logout', views.LogoutView.as_view(), name='logout'),
      # path('', login_required(views.HomeView.as_view()), name='home'),
      path('activate/<uidb64>/<token>',
            views.ActivateAccountView.as_view(), name='activate'),
      # path('set-new-password/<uidb64>/<token>',
      #       views.SetNewPasswordView.as_view(), name='set-new-password'),
      # path('request-reset-email', views.RequestResetEmailView.as_view(),
      #       name='request-reset-email'),
      path('<int:pk>/profile/', views.profilepageview, name="profile_page"),
      path('user_list/', views.User_List, name='user_list'),
      path("search/", views.UserSearch.as_view(), name="search"),



      # password reset when user isnt logged in 
      path(
            "reset_password/",
            auth_views.PasswordResetView.as_view(
                  template_name="accounts/password_reset_form.html"
            ),
            name="password_reset",
      ),
      path(
            "reset_password_sent/",
            auth_views.PasswordResetDoneView.as_view(
                  template_name="accounts/password_reset_done.html"
            ),
            name="password_reset_done",
      ),
      path(
            "reset/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(
                  template_name="accounts/password_reset_confirm.html"
            ),
            name="password_reset_confirm",
      ),
      path(
            "reset_password_complete/",
            auth_views.PasswordResetCompleteView.as_view(
                  template_name="accounts/password_reset_complete.html"
            ),
            name="password_reset_complete",
      ),
]
























# from django.urls import path         
# from .views import UserRegisterView, user_registration, RegistrationView, profilepageview, User_List, UserSearch, login, signup
# from django.contrib.auth.views import LoginView


                                                                           
# urlpatterns = [
#    # path('register/', UserRegisterView.as_view(), name='register'),
#    path('register/', RegistrationView.as_view(), name='register'),
#    # path('register/', signup, name='register'),
#    # path('register/', user_registration, name='register'),
#    path('login/', LoginView.as_view(), name="login"),
#    # path('login/', login, name="login"),
#    # path('<int:pk>/profile/', ProfilePageView.as_view(), name="profile_page")
#    path('<int:pk>/profile/', profilepageview, name="profile_page"),
#    path('user_list/', User_List, name='user_list'),
#    path("search/", UserSearch.as_view(), name="search")
# ] 