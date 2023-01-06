from django.test import TestCase
from django.urls import reverse
from users.models import User, UserProfile
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.token import generate_token


class BaseTest(TestCase):
    def setUp(self):
        # self.register_url=reverse('register')
        # self.login_url=reverse('login')
        # self.profile_page_url=reverse('profile_page')
        # self.request_reset_email_url=reverse('request-reset-email')

        self.user={
            'user':'username',
            'email': 'email@email.com',
            'password': 'password123'
        }
        self.invalid_email={
            'username':'admin', 
            'email': '', 
            'password': "password123"
        }
        self.invalid_username={
            'username':'',
            'email': 'e@e.com',
            'password': 'password123'
        }
        # self.user_short_password={
        #     'email':'testemail@gmail.com',
        #     'username':'username',
        #     'password':'tes',
        #     'password2':'tes',
        #     'name':'fullname'
        # }
        # self.user_unmatching_password={
        #     'email':'testemail@gmail.com',
        #     'username':'username',
        #     'password':'teslatt',
        #     'password2':'teslatto',
        #     'name':'fullname'
        # }

        # self.user_invalid_email={
        #     'email':'test.com',
        #     'username':'username',
        #     'password':'teslatt',
        #     'password2':'teslatto',
        #     'name':'fullname'
        # }
        # self.incorrect_request_reset_email={
        #     'email':'test.com',
        # }
        return super().setUp()


class MyAccountManagerTest(BaseTest):
    # def test_can_view_page_correctly(self):
    #    response=self.client.get(self.register_url)
    #    self.assertEqual(response.status_code,200)
    #    self.assertTemplateUsed(response,'auth/register.html')

    # def test_can_register_user(self):
    #     response=self.client.post(self.register_url, self.user, format='text/html')
    #     self.assertEqual(response.status_code, 302)

    # def test_cant_register_user_withshortpassword(self):
    #     response=self.client.post(self.register_url, self.user_short_password, format='text/html')
    #     self.assertEqual(response.status_code, 400)

    # def test_cant_register_user_with_unmatching_passwords(self):
    #     response=self.client.post(self.register_url, self.user_unmatching_password, format='text/html')
    #     self.assertEqual(response.status_code, 400)

    # def test_cant_register_user_with_invalid_email(self):
    #     response=self.client.post(self.register_url, self.user_invalid_email, format='text/html')
    #     self.assertEqual(response.status_code, 400)

    # def test_cant_register_user_with_taken_email(self):
    #     self.client.post(self.register_url, self.user, format='text/html')
    #     response=self.client.post(self.register_url, self.user, format='text/html')
    #     self.assertEqual(response.status_code, 400)

    def test_create_user(self):
        response=self.client.post(self.invalid_email, format='text/html')
        # self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_code("User must have an email"), 404)
        # self.assertTrue("Users must have an email" in response.content)

    def test_create_superuser(self):
        response=self.client.post(self.user, format='text/html')
        # self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_code("User must have an email"), 404)
        # self.assertTrue("Users must have an email" in response.content)