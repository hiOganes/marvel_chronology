from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.movies.models import Movies
from api.movies_v1.data_tests import new_movie, update_movie
from apps.accounts.data_tests import user_sign_up, user_sign_in, user_invalid


class TestLogOut(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.url = reverse('custom-logout')

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class TestSignUpView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_user_regiser_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_user_register(self):
        amount_users_before = get_user_model().objects.count()
        response = self.client.post(self.url, data=user_sign_up)
        amount_users_after = get_user_model().objects.count()
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(amount_users_before < amount_users_after)


class TestPasswordResetView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('password_reset')
        self.user = get_user_model().objects.all()[0]

    def test_send_reset_email(self):
        response = self.client.post(self.url, data={'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTemplateUsed('password_reset_done.html')