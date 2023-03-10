from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from users.token import generate_token
from django.core.mail import EmailMessage
from django.core import mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .models import User, UserProfile
from family_budget.models import Project
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.db.models import Q
from users.tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from .forms import SignUpForm
from rest_framework.decorators import api_view
import threading

# def register(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = "Activate your blog account."
#             message = render_to_string(
#                 "registration/email_template.html",
#                 {
#                     "user": user,
#                     "domain": current_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": account_activation_token.make_token(user),
#                 },
#             )
#             to_email = form.cleaned_data.get("email")
#             email = mail.EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return render(request, "registration/confirm_email.html")
#     else:
#         form = SignUpForm()
#     return render(request, "registration/register.html", {"form": form})


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        # self.email.send()
        self.email_message.send()


# def RegistrationView(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)     
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = "Activate your blog account."
#             message = render_to_string(
#                 "auth/email_template.html",
#                 {
#                     "user": user,
#                     "domain": current_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": account_activation_token.make_token(user),
#                 },
#             )
#             to_email = form.cleaned_data.get("email")
#             email = mail.EmailMessage(mail_subject, message, to=[to_email])
#             email.send()
#             return render(request, "auth/confirm_email.html")
#     else:
#         form = SignUpForm()
#     return render(request, "auth/register.html", {"form": form})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        email = request.POST.get('email')
        username = request.POST.get('username')
        full_name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'passwords should be atleast 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR, 'passwords dont match')
            context['has_error'] = True
        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Please provide a valid email')
            context['has_error'] = True
        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken')
                context['has_error'] = True
        except Exception as identifier:
            pass
        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'auth/register.html', context, status=400)


        user = User.objects.create_user(username=username, email=email, password=password)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = 'Active your Account'
        message = render_to_string('auth/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   }
                                   )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS,
                             'Check your email for confirmation link!')

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'auth/login.html', status=401, context=context)
        login(request, user)
        return redirect('home')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('login')
        return render(request, 'auth/activate_failed.html', status=401)


# class HomeView(View):
#     def get(self, request):
#         return render(request, 'budget/home.html')


# class LogoutView(View):
#     def post(self, request):
#         logout(request)
#         messages.add_message(request, messages.SUCCESS, 'Logout successfully')
#         return redirect('login')


# class RequestResetEmailView(View):
#     def get(self, request):
#         return render(request, 'auth/request-reset-email.html')

#     def post(self, request):
#         email = request.POST['email']

#         if not validate_email(email):
#             messages.error(request, 'Please enter a valid email')
#             return render(request, 'auth/request-reset-email.html')

#         user = User.objects.filter(email=email)

#         if user.exists():
#             current_site = get_current_site(request)
#             email_subject = '[Reset your Password]'
#             message = render_to_string('auth/reset-user-password.html',
#                                        {
#                                            'domain': current_site.domain,
#                                            'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                                            'token': PasswordResetTokenGenerator().make_token(user[0])
#                                        }
#                                        )

#             email_message = EmailMessage(
#                 email_subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [email]
#             )

#             EmailThread(email_message).start()

#         messages.success(
#             request, 'We have sent you an email with instructions on how to reset your password')
#         return render(request, 'auth/request-reset-email.html')


# class SetNewPasswordView(View):
#     def get(self, request, uidb64, token):
#         context = {
#             'uidb64': uidb64,
#             'token': token
#         }

#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))

#             user = User.objects.get(pk=user_id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 messages.info(
#                     request, 'Password reset link, is invalid, please request a new one')
#                 return render(request, 'auth/request-reset-email.html')

#         except DjangoUnicodeDecodeError as identifier:
#             messages.success(
#                 request, 'Invalid link')
#             return render(request, 'auth/request-reset-email.html')

#         return render(request, 'auth/set-new-password.html', context)

#     def post(self, request, uidb64, token):
#         context = {
#             'uidb64': uidb64,
#             'token': token,
#             'has_error': False
#         }

#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         if len(password) < 6:
#             messages.add_message(request, messages.ERROR,
#                                  'passwords should be at least 6 characters long')
#             context['has_error'] = True
#         if password != password2:
#             messages.add_message(request, messages.ERROR,
#                                  'passwords don`t match')
#             context['has_error'] = True

#         if context['has_error'] == True:
#             return render(request, 'auth/set-new-password.html', context)

#         try:
#             user_id = force_str(urlsafe_base64_decode(uidb64))

#             user = User.objects.get(pk=user_id)
#             user.set_password(password)
#             user.save()

#             messages.success(
#                 request, 'Password reset success, you can login with new password')

#             return redirect('login')

#         except DjangoUnicodeDecodeError as identifier:
#             messages.error(request, 'Something went wrong')
#             return render(request, 'auth/set-new-password.html', context)

#         return render(request, 'auth/set-new-password.html', context)



def profilepageview(request, pk, *args, **kwargs):
    if request.method == 'GET':
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        p = Paginator(Project.objects.filter(author=user), 2)
        page = request.GET.get("page")
        projects = p.get_page(page)

        context = {
            'projects':projects,
            'user':user,
            'profile':profile
        }

        return render(request, "registration/profile_page.html", context)


    if request.method == 'DELETE':
        id = json.loads(request.body)['id']
        project = Project.objects.get(id=id)
        project.delete()
        return HttpResponse('')


def User_List(request):
    users = User.objects.all() 
    return render(request, 'registration/user_list.html', {'users':users})


class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        profile_list = UserProfile.objects.filter(Q(user__username__icontains=query))
        # budget = Project.objects.filter(Q(user__project__icontains=query))
        context = {
            "profile_list": profile_list,
        }
        return render(request, "registration/search.html", context)
















































































# from django.shortcuts import render							
# from django.views import generic 						
# from django.contrib.auth.forms import UserCreationForm                                                                                          
# from django.urls import reverse_lazy     
# from .models import User, UserProfile
# from .forms import SignUpForm         
# from family_budget.models import Project, Expense, Category         
# from django.views.generic import CreateView, DeleteView, DetailView, ListView, View  															 
# from django.core.paginator import Paginator
# from django.http import HttpResponseRedirect, HttpResponse
# import json
# from django.db.models import Q
# from knox.views import LoginView as KnoxLoginView
# from django.shortcuts import render, redirect
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import render, redirect
# from django.views.generic import View
# from django.contrib import messages
# # from validate_email import validate_email
# from django.contrib.auth.models import User
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# # from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
# # from .utils import generate_token
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# import threading


# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'registration/register.html')

#     def post(self, request):
#         context = {

#             'data': request.POST,
#             'has_error': False
#         }

#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         # full_name = request.POST.get('name')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         # if len(password) < 6:
#         #     messages.add_message(request, messages.ERROR,
#         #                          'passwords should be atleast 6 characters long')
#         #     context['has_error'] = True
#         # if password != password2:
#         #     messages.add_message(request, messages.ERROR,
#         #                          'passwords dont match')
#         #     context['has_error'] = True

#         # if not validate_email(email):
#         #     messages.add_message(request, messages.ERROR,
#         #                          'Please provide a valid email')
#         #     context['has_error'] = True

#         # try:
#         #     if User.objects.get(email=email):
#         #         messages.add_message(request, messages.ERROR, 'Email is taken')
#         #         context['has_error'] = True

#         # except Exception as identifier:
#         #     pass

#         # try:
#         #     if User.objects.get(username=username):
#         #         messages.add_message(
#         #             request, messages.ERROR, 'Username is taken')
#         #         context['has_error'] = True

#         # except Exception as identifier:
#         #     pass

#         # if context['has_error']:
#         #     return render(request, 'auth/register.html', context, status=400)

#         user = User.objects.create_user(username=username, email=email)
#         user.set_password(password)
#         # user.first_name = full_name
#         # user.last_name = full_name
#         user.is_active = False
#         user.save()

#         # current_site = get_current_site(request)
#         # email_subject = 'Active your Account'
#         # message = render_to_string('auth/activate.html',
#         #                            {
#         #                                'user': user,
#         #                                'domain': current_site.domain,
#         #                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         #                                'token': generate_token.make_token(user)
#         #                            }
#         #                            )

#         # email_message = EmailMessage(
#         #     email_subject,
#         #     message,
#         #     settings.EMAIL_HOST_USER,
#         #     [email]
#         # )

#         # EmailThread(email_message).start()
#         # messages.add_message(request, messages.SUCCESS,
#         #                      'account created succesfully')

#         return redirect('login')

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()  
#             # load the profile instance created by the signal
#             user.save()
#             raw_password = form.cleaned_data.get('password1')

#             # login user after signing up
#             user = authenticate(username=user.username, password=raw_password)
#             login(request, user)

#             # redirect user to home page
#             return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/register.html', {'form': form})

# class UserRegisterView(generic.CreateView):                  
# 	form_class = SignUpForm                            		                       
# 	template_name = 'registration/register.html'             
# 	success_url = reverse_lazy('login') 
	

# def user_registration(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         user_model = get_user_model()
#         user_obj = user_model.objects.create_user(email=email, username=username, password=password)
#         user_obj.set_password(password)
#         user_obj.save()
#         user_auth = authenticate(username=username, password=password)
#         login(request, user_auth)
#         return redirect('home')
#     else:
#         return render(request, 'registration/register.html')


# # class ProfilePageView(DetailView, ListView):
# #     def get(self, request, pk, *args, **kwargs):
# #         profile = UserProfile.objects.get(pk=pk)
# #         user = profile.user
# #         p = Paginator(Project.objects.filter(author=user), 1)
# #         page = request.GET.get("page")
# #         projects = p.get_page(page)

# #         context = {
# #             'projects':projects,
# #             'user':user,
# #             'profile':profile
# #         }

# #         if request.method == 'DELETE':
# #             id = json.loads(request.body)['id']
# #             project = Project.objects.get(id=id)
# #             project.delete()
# #             return HttpResponse('')

# #         return render(request, "registration/profile_page.html", context)


# def profilepageview(request, pk, *args, **kwargs):
#     if request.method == 'GET':
#         profile = UserProfile.objects.get(pk=pk)
#         user = profile.user
#         p = Paginator(Project.objects.filter(author=user), 2)
#         page = request.GET.get("page")
#         projects = p.get_page(page)

#         context = {
#             'projects':projects,
#             'user':user,
#             'profile':profile
#         }

#         return render(request, "registration/profile_page.html", context)


#     if request.method == 'DELETE':
#         id = json.loads(request.body)['id']
#         project = Project.objects.get(id=id)
#         project.delete()
#         return HttpResponse('')


# def User_List(request):
#     users = User.objects.all() 
#     return render(request, 'registration/user_list.html', {'users':users})


# class UserSearch(View):
#     def get(self, request, *args, **kwargs):
#         query = self.request.GET.get("query")
#         profile_list = UserProfile.objects.filter(Q(user__username__icontains=query))
#         # budget = Project.objects.filter(Q(user__project__icontains=query))
#         context = {
#             "profile_list": profile_list,
#         }
#         return render(request, "registration/search.html", context)


# # def login(request):
# # 	if request.method == 'POST':
# # 		username = request.POST['username']
# # 		password = request.POST['password']
# # 		user_auth = authenticate(username=username, password=password)
# # 		login(request, user_auth)
# # 		return redirect('home')
# # 	else:
# # 		return render(request, 'registration/login.html')


# def user_logout(request):
# 	logout(request)
# 	return redirect('home')