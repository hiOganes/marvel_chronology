import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status

from conftest import login_data


@pytest.mark.django_db()
class TestMoviesCreatedView:
    client = Client()
    url = reverse('movies-created')

    def test_movies_created_status_code(self, login_data):
        self.client.login(**login_data['superuser'])
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_movies_created_template(self, login_data):
        self.client.login(**login_data['superuser'])
        response = self.client.get(self.url)
        asserts.assertTemplateUsed(response, 'movies/created.html')
