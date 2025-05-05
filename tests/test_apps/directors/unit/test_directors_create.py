import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status
from pytest_django import asserts
from django.core.exceptions import ValidationError

from apps.movies.models import Movies
from apps.directors.models import Directors
from conftest import login_data


@pytest.fixture
def new_movie():
    data = {
        'first_name': 'first_name',
        'last_name': 'last_name',
    }
    return data


@pytest.mark.django_db()
class TestCreateDirectorsView:
    client = Client()
    model = Movies
    url = reverse('directors-create')

    def test_create_directors_status_code_get(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_create_directors_status_code_post(self, new_movie):
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_302_FOUND

    def test_create_directors_status_code_get_user(self, login_data):
        self.client.login(**login_data['user'])
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_directors_status_code_post_user(self, new_movie, login_data):
        self.client.login(**login_data['user'])
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_directors_status_code_get_superuser(self, login_data):
        self.client.login(**login_data['superuser'])
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_directors_status_code_post_superuser(self, new_movie,
                                                      login_data):
        self.client.login(**login_data['superuser'])
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_302_FOUND

