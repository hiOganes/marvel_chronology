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
def get_url():
    movie = Movies.objects.all()[0]
    return reverse('movies-delete', kwargs={'pk': movie.pk})


@pytest.mark.django_db()
class TestDeleteMoviesView:
    client = Client()
    model = Movies

    def test_delete_movies_status_code_get(self, get_url):
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_delete_movies_status_code_get_user(self, login_data, get_url):
        self.client.login(**login_data['user'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_movies_status_code_get_superuser(self, login_data, get_url):
        self.client.login(**login_data['superuser'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_delete_movies_count_get_superuser(self, login_data, get_url):
        self.client.login(**login_data['superuser'])
        movies_before = Movies.objects.count()
        response = self.client.get(get_url)
        movies_after = Movies.objects.count()
        assert movies_before > movies_after
