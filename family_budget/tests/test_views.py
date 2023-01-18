from django.test import TestCase
from django.urls import reverse
from users.models import User, UserProfile
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.token import generate_token


class BaseTest(TestCase):
    def setUp(self):
        self.home_url=reverse('home')
        return super().setUp()
    
class Home(BaseTest):
    def test_home_page(self):
        response=self.client.get(self.home_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'budget/home.html')
    

# class RegisterTest(BaseTest):
#     def test_can_view_page_correctly(self):
#        response=self.client.get(self.register_url)
#        self.assertEqual(response.status_code,200)
#        self.assertTemplateUsed(response,'auth/register.html')

#     def test_can_register_user(self):
#         response=self.client.post(self.register_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 302)

#     def test_cant_register_user_withshortpassword(self):
#         response=self.client.post(self.register_url, self.user_short_password, format='text/html')
#         self.assertEqual(response.status_code, 400)

#     def test_cant_register_user_with_unmatching_passwords(self):
#         response=self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
#         self.assertEqual(response.status_code, 400)

#     def test_cant_register_user_with_invalid_email(self):
#         response=self.client.post(self.register_url, self.user_invalid_email, format='text/html')
#         self.assertEqual(response.status_code, 400)

#     def test_cant_register_user_with_taken_email(self):
#         self.client.post(self.register_url, self.user, format='text/html')
#         response=self.client.post(self.register_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 400)

# class LoginTest(BaseTest):
#     def test_can_access_page(self):
#         response=self.client.get(self.login_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'auth/login.html')

#     def test_login_success(self):
#         self.client.post(self.register_url, self.user, format='text/html')
#         user=User.objects.filter(email=self.user['email']).first()
#         user.is_active=True
#         user.save()
#         response= self.client.post(self.login_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 302)

#     def test_cant_login_with_unverified_email(self):
#         self.client.post(self.register_url, self.user,format='text/html')
#         response= self.client.post(self.login_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 401)

#     def test_cant_login_with_no_username(self):
#         response= self.client.post(self.login_url, {'password':'passwped','username':''}, format='text/html')
#         self.assertEqual(response.status_code, 401)

#     def test_cant_login_with_no_password(self):
#         response= self.client.post(self.login_url, {'username':'passwped','password':''}, format='text/html')
#         self.assertEqual(response.status_code, 401)

# class UserVerifyTest(BaseTest):
#     def test_user_activates_success(self):
#         user=User.objects.create_user('crytest@gmail.com', 'testuser', 'password12345!')
#         user.set_password('password12345!')
#         user.is_active=False
#         user.save()
#         uid=urlsafe_base64_encode(force_bytes(user.pk))
#         token=generate_token.make_token(user)
#         response=self.client.get(reverse('activate', kwargs={'uidb64':uid, 'token':token}))
#         self.assertEqual(response.status_code,302)
#         user=User.objects.get(email='crytest@gmail.com')
#         self.assertTrue(user.is_active)

#     def test_user_cant_activates_succesfully(self):
#         user=User.objects.create_user('crytest@gmail.com', 'testuser', 'password12345!')
#         user.set_password('password12345!')
#         user.is_active=False
#         user.save()
#         # uid=urlsafe_base64_encode(force_bytes(user.pk))
#         # token=generate_token.make_token(user)
#         response=self.client.get(reverse('activate', kwargs={'uidb64':'uid', 'token':'token'}))
#         self.assertEqual(response.status_code,401)
#         user=User.objects.get(email='crytest@gmail.com')
#         self.assertFalse(user.is_active)

# class UserProfileTest(BaseTest):
#     def test_can_access_a_profile_page(self):
#         self.client.post(self.register_url, self.user, format='text/html')
#         user=User.objects.filter(email=self.user['email']).first()
#         user.is_active=True
#         user.save()
#         response= self.client.post(self.login_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 302)
#         response=self.client.get('/users/1/profile/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/profile_page.html')

# class UserListTest(BaseTest):
#     def test_can_return_user_list(self):
#         # user_list=User.objects.all()
#         response=self.client.get('/users/user_list/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/user_list.html')

# class UserSearchTest(BaseTest):
#     def test_can_return_user_list(self):
#         # # user_list=User.objects.all()
#         # response= self.client.post(self.search, self.user, format='text/html')
#         # self.assertEqual(response.status_code, 302)
#         response=self.client.get('/users/search/?query=ad')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'registration/search.html')
    



# class BaseTest(TestCase):
#     def setUp(self):
#         self.request_reset_email_url=reverse('request-reset-email')
#         self.user={
#             'email':'testemail@gmail.com',
#             'username':'username',
#             'password':'password',
#             'password2':'password',
#             'name':'fullname'
#         }
#         # self.login_url=reverse('login')

# class Request_Reset_Email_Test(BaseTest):
#     def test_can_view_page_correctly(self):
#         response=self.client.get(self.request_reset_email_url)
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed(response,'auth/request-reset-email.html')

#     def test_email_post(self):
#         response=self.client.post(self.request_reset_email_url, self.user, format='text/html')
#         self.assertEqual(response.status_code, 200)

#     # def test_if_not_validate_email(self):
#     #     # response=self.client.post(self.request_reset_email_url, self.incorrect_request_reset_email, format='text/html')
#     #     # self.assertEqual(response.status_code, 400)
#     #     # response=self.client.get(self.request_reset_email_url)
#     #     response = self.client.post('Please enter a valid email')
#     #     self.assertEqual(response.status_code,200)
#     #     self.assertTemplateUsed(response,'auth/request-reset-email.html')

#     # def test_if_not_validate_email(self):
#     #     response=self.client.post(self.request_reset_email_url, self.incorrect_request_reset_email, format='text/html')
#     #     self.assertEqual(response.status_code, 400)

#     def test_if_not_validate_email(self):
#         response = self.client.post(self.request_reset_email_url, "Please enter a valid email", {'email': "adminmp.com"})
#         self.assertTrue('"error": true' in response.content)