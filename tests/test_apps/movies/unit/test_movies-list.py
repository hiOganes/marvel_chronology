import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestListMoviesView:
    client = Client()
    url = reverse('movies-list')

    def test_list_movies_status_code(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_movies_template(self):
        response = self.client.get(self.url)
        asserts.assertTemplateUsed(response, 'movies/list.html')

    def test_list_movies_pagination(self):
        response = self.client.get(self.url)
        assert len(response.context['pages_movies']) == 10
