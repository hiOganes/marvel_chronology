from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.db import connection

from api.movies_v1 import views
from api.movies_v1.data_tests import new_movie
from apps.movies.models import Movies


class TestListMoviesAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.url = reverse('api-movies-list')
        self.view = views.ListMoviesAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_movies_list_and_pagination(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'])

    def test_movies_list_and_search(self):
        with connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
        request = self.factory.get(self.url, data={'search': 'Avengers'})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Movies.objects.count() > response.data['count'])

    def test_movies_list_create_anonymous(self):
        request = self.factory.post(self.url, new_movie(), format='multipart')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_movies_list_create_user(self):
        request = self.factory.post(self.url, new_movie(), format='multipart')
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movies_list_create_superuser(self):
        request = self.factory.post(self.url, new_movie(), format='multipart')
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movies_list_create_invalid_data(self):
        edit_movie = new_movie()
        edit_movie['position'] = 'string'
        request = self.factory.post(self.url, edit_movie, format='multipart')
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movies_list_create_empty_data(self):
        request = self.factory.post(self.url, {}, format='multipart')
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDetailMoviesAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.movie = Movies.objects.all()[0]
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.url = reverse('api-movies-detail', kwargs={'pk': self.movie.pk})
        self.view = views.DetailMoviesAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_movies_detail(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



