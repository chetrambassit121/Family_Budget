from django.test import TestCase
from django.urls import reverse
from users.models import User, UserProfile
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.token import generate_token




class LoginHtmlUrlTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     number_of_users = 30
    #     for user_id in range(number_of_users):
    #         User.objects.create(username=f"User1{user_id}", email=f"email@gmail.com{user_id}", fullname='John Doe{user_id}', password='password12345!{user_id}')

    def test_url_exists(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    # def test_pagination_is_correct(self):
    #     response = self.client.get(reverse('students'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] is True)
    #     self.assertEqual(len(response.context['student_list']), 10)



class RegisterHtmlUrlTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     number_of_users = 30
    #     for user_id in range(number_of_users):
    #         User.objects.create(username=f"User1{user_id}", email=f"email@gmail.com{user_id}", fullname='John Doe{user_id}', password='password12345!{user_id}')

    def test_url_exists(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    # def test_pagination_is_correct(self):
    #     response = self.client.get(reverse('students'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] is True)
    #     self.assertEqual(len(response.context['student_list']), 10)