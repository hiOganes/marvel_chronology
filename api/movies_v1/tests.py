from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import QueryDict

from api.movies_v1 import views
# from api.movies_v1.data_tests import new_movie
from apps.movies.models import Movies


class TestListMoviesAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.url = reverse('api-movies-list')
        self.view = views.ListMoviesAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_movies_list_and_pagination(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'])

    def test_movies_list_and_search(self):
        request = self.factory.get(self.url)
        request.query_params = QueryDict('', mutable=True)
        request.query_params.update({'search': 'Avengers'})
        print(request.query_params)
        response = self.view(request)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
