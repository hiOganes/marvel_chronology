from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.directors.models import Directors
from api.directors_api.data_tests import new_director


class TestCreateDirectorsView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('directors-create')
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]

    def test_create_directors_status_code_get_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_directors_status_code_post_anonymous(self):
        response = self.client.post(self.url, data=new_director)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_directors_status_code_get_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_directors_status_code_post_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=new_director)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_directors_status_code_get_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_directors_status_code_post_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data=new_director)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
