from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import QueryDict
from django.db import connection

from api.movies_api import views
from api.movies_api.data_tests import new_movie, update_movie
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

    def test_movies_get_movie(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movies_update_movie_anonymous(self):
        request = self.factory.patch(self.url, update_movie)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_movies_update_movie_user(self):
        request = self.factory.patch(self.url, update_movie)
        force_authenticate(request, self.user)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_movies_update_movie_superuser(self):
        request = self.factory.patch(self.url, update_movie)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movies_update_movie_invalid_data(self):
        invalid_data = {'position': 'string'}
        request = self.factory.patch(self.url, invalid_data)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movies_update_movie_empty_data(self):
        request = self.factory.patch(self.url, {'title_ru': ''})
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movies_delete_moive_anonymous(self):
        amount_before = Movies.objects.count()
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.movie.pk)
        amount_after = Movies.objects.count()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(amount_before == amount_after)

    def test_movies_delete_moive_user(self):
        amount_before = Movies.objects.count()
        request = self.factory.delete(self.url)
        force_authenticate(request, self.user)
        response = self.view(request, pk=self.movie.pk)
        amount_after = Movies.objects.count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(amount_before == amount_after)

    def test_movies_delete_moive_superuser(self):
        amount_before = Movies.objects.count()
        request = self.factory.delete(self.url)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=self.movie.pk)
        amount_after = Movies.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(amount_before > amount_after)

    def test_movies_delete_movie_invalid_data(self):
        amount_before = Movies.objects.count()
        request = self.factory.delete(self.url)
        force_authenticate(request, self.superuser)
        response = self.view(request, pk=10**10)
        amount_after = Movies.objects.count()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(amount_before == amount_after)


class TestViewedAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.movie = Movies.objects.all()[0]
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]
        self.url = reverse('api-viewed-status')
        self.view = views.ViewedAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_movies_update_viewed_anonymous(self):
        request = self.factory.post(self.url, data={'id': self.movie.pk})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_movies_update_viewed_user(self):
        request = self.factory.post(self.url, data={'id': self.movie.pk})
        force_authenticate(request, self.user)
        response = self.view(request)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        )

    def test_movies_update_viewed_superuser(self):
        request = self.factory.post(self.url, data={'id': self.movie.pk})
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
        )

    def test_movies_update_viewed_invalid_data(self):
        request = self.factory.post(self.url, data={'id': 10**10})
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_movies_update_viewed_empty_data(self):
        request = self.factory.post(self.url, data={})
        force_authenticate(request, self.superuser)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)