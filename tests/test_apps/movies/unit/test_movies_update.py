from datetime import datetime

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
def new_data():
    data = {
        'position': 1,
        'title_ru': 'Фильм',
        'title_en': 'Film',
    }
    return data

@pytest.fixture
def get_url():
    movie = Movies.objects.all()[0]
    return reverse('movies-update', kwargs={'pk': movie.pk})


@pytest.mark.django_db()
class TestUpdateMoviesView:
    client = Client()
    model = Movies

    def test_update_movies_status_code_get(self, get_url):
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_update_movies_status_code_post(self, new_data, get_url):
        response = self.client.post(get_url, data=new_data)
        assert response.status_code == status.HTTP_302_FOUND

    def test_update_movies_status_code_get_user(self, login_data, get_url):
        self.client.login(**login_data['user'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_movies_status_code_post_user(self, new_data, login_data, get_url):
        self.client.login(**login_data['user'])
        response = self.client.post(get_url, data=new_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_movies_status_code_get_superuser(self, login_data, get_url):
        self.client.login(**login_data['superuser'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_200_OK

    def test_update_movies_status_code_post_superuser(self, new_data,
                                                      login_data, get_url):
        self.client.login(**login_data['superuser'])
        response = self.client.post(get_url, data=new_data)
        assert response.status_code == status.HTTP_200_OK

