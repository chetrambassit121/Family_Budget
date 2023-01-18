from django.test import TestCase
from django.urls import reverse
from users.models import User, UserProfile
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.token import generate_token
from users.models import MyAccountManager
from django.contrib.auth import get_user_model



class BaseTest(TestCase):
    def setUp(self):            
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        # self.profile_page_url=reverse('profile_page')
        # self.request_reset_email_url=reverse('request-reset-email')
        self.user={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'password',
            'password2':'password',
            'name':'fullname',
            'pk':1
        }
        self.user_profile={
            'user':'username',
            'pk':1
        }
        self.myaccountmanager = MyAccountManager()
        return super().setUp()
    # def setUp(self):            
    #     # self.register_url=reverse('register')
    #     # self.login_url=reverse('login')
    #     # self.profile_page_url=reverse('profile_page')
    #     # self.request_reset_email_url=reverse('request-reset-email')

    #     self.user={
    #         'email':'testemail@gmail.com',
    #         'username':'username',
    #         'password':'password',
    #         'password2':'password',
    #         'name':'fullname',
    #         'pk':1
    #     }
    #     self.invalid_email={
    #         'username':'admin', 
    #         'email': '', 
    #         'password': "password123"
    #     }
    #     self.invalid_username={
    #         'username':'',
    #         'email': 'e@e.com',
    #         'password': 'password123'
    #     }
    #     self.myaccountmanager = MyAccountManager()
    #     # self.userprofile_url=reverse('users//1/profile_page')
    #     self.register_url=reverse('register')
    #     self.login_url=reverse('login')
        
    #     return super().setUp()
    



class MyAccountManagerTest(BaseTest):            
    def test_create_user_email_value_error(self):
        with self.assertRaises(ValueError):
            self.myaccountmanager.create_user('', 'adminuser', 'passw0rd')

            
    def test_create_user_username_value_error(self):
        with self.assertRaises(ValueError):
            self.myaccountmanager.create_user('email@email.com', '', 'passw0rd')
        
    def test_create_superuser(self):
        # model = get_user_model()
        user = get_user_model().objects.create_superuser('e@e.com', 'adminuser', 'passw0rd')
        # self.create_user()
        # user = self.create_user()
        assert user.pk is not None
        assert user.is_staff
        assert user.is_admin
        assert user.is_superuser
        user.save()
        

class User(BaseTest):
    # model = get_user_model()
    # user = model.objects.create_user('e@e.com', 'adminuser', 'passw0rd')
    def test_str(self):
        # model = get_user_model()
        user = get_user_model().objects.create_user('e@e.com', 'adminuser', 'passw0rd')
        self.assertEqual(str(user), user.username)
        
    def test_has_perm(self):
        # model = get_user_model()
        user = get_user_model().objects.create_superuser('e@e.com', 'adminuser', 'passw0rd')
        self.assertEqual(user.has_perm('auth.test'), True)
        
    def test_has_module_perms(self):
        # model = get_user_model()
        user = get_user_model().objects.create_superuser('e@e.com', 'adminuser', 'passw0rd')
        self.assertEqual(user.has_module_perms('auth.test'), True)
        
    # def test_markdown_to_html():
    #     user = get_user_model().objects.create_user('e@e.com', 'adminuser', 'passw0rd')
    #     username = get_user_model.objects.get(user.username)
    #     markdown = '#test'
    #     html = markdown_to_html(markdown)
    #     assert html == '<h1>test</h1>\n'
        


# class UserProfile(BaseTest):
#     def test_profile_str(self):
#         user = get_user_model().objects.create_user('e@e.com', 'adminuser', 'passw0rd')
#         userprofile=get_user_model().objects.create_user_profile('user', 1)
#         self.assertEqual(str(userprofile), userprofile.user)
        
        
        
        
        # self.client.post(self.register_url, self.user, format='text/html')
        # user=get_user_model().objects.filter(email=self.user['email']).first()
        # user.is_active=True
        # user.save()
        # userprofile=get_user_model().objects.create_user_profile('username', 1)
        # response= self.client.post(self.login_url, self.user, format='text/html')
        # self.assertEqual(response.status_code, 302)
        # response=self.client.get('/users/1/profile/')
        # self.assertEqual(str(user), user.username)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'registration/profile_page.html')
        # self.assertEqual(str(user), user.username)
        # user = get_user_model().objects.create_user('e@e.com', 'adminuser', 'passw0rd')
        # userprofile = get_user_model().objects.get(user.userprofile)
        # self.assertEqual(str(user), user.username)
    

        # model = get_user_model()
        # user = model.objects.create_user('e@e.com', 'adminuser', 'passw0rd')
        # userprofile = user.objects.get(user.username)
        # self.assertEqual(str(userprofile), user.username)
        
        
        
        
        # self.client.post(self.register_url, self.user, format='text/html')
        # model = get_user_model()
        # user=model.objects.filter(email=self.user['email']).first()
        # user.is_active=True
        # user.save()
        # response= self.client.post(self.login_url, self.user, format='text/html')
        # self.assertEqual(response.status_code, 302)
        # response=self.client.get('/users/1/profile/')
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'registration/profile_page.html') 
        # self.assertEqual(str(user), user.username)
        
# class UserProfile(BaseTest):
#     # def test_get_absolute_url(self):
#     #     model = get_user_model()
#     #     user = model.objects.create_user('e@e.com', 'adminuser', 'passw0rd')
#     #     # response= self.client.post(self.login_url, user, format='text/html')
#     #     # self.assertEqual(response.status_code, 302)
#     #     # response=self.client.get('/users/1/profile/')
#     #     # user = self.client.post(self.register_url, self.user, format='text/html')
#     #     self.assertEquals(user.get_absolute_url(), "/users/1/profile_page")
        
        
#     def test_userprofile_str(self):
#         self.client.post(self.register_url, self.user, format='text/html')
#         user=User.objects.filter(email=self.user['email']).first()
#         user.is_active=True
#         user.save()
#         response= self.client.post(self.login_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 302)
#         response=self.client.get('/users/1/profile/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/profile_page.html')
#         # self.assertEqual(str(user), user)
        
        
#         # self.client.post(self.register_url, self.user, format='text/html')
#         # user=User.objects.filter(email=self.user['email']).first()
#         # user.is_active=True
#         # user.save()
#         # response= self.client.post(self.login_url, self.user, format='text/html')
#         # self.assertEqual(response.status_code, 302)
#         # response=self.client.get('/users/1/profile/')
#         # self.assertEquals(user.get_absolute_url(), "/users/1/profile_page")
        

