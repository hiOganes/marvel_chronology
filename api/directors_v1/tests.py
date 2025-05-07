from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from api.directors_v1 import views
from api.directors_v1.data_tests import new_director
from apps.directors.models import Directors


class TestCreateDirectorsAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.url = reverse('api-directors-create')
        self.factory = APIRequestFactory()
        self.view = views.CreateDirectorsAPIView.as_view()

    def test_create_director_user(self):
        request = self.factory.post(self.url, new_director)
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_director_superuser(self):
        request = self.factory.post(self.url, new_director)
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_director_epty_data(self):
        request = self.factory.post(self.url, {})
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteDirectorsAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.director = Directors.objects.all()[0]
        self.url = reverse(
            'api-directors-delete',
            kwargs={'pk': self.director.pk}
        )
        self.factory = APIRequestFactory()
        self.view = views.DeleteDirectorsAPIView.as_view()

    def test_delete_director_user(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, self.user)
        response = self.view(request, pk=self.director.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_director_superuser(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.director.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_director_ivalid_pk(self):
        request = self.factory.delete(self.url)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=10**10)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
