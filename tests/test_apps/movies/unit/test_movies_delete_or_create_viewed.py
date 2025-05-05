import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.movies.models import Movies


@pytest.fixture
def get_url():
    movie = Movies.objects.all()[0]
    return reverse('movies-viewed', kwargs={'pk': movie.pk})


@pytest.mark.django_db()
class TestDeleteOrCreateViewedView:
    client = Client()
    model = Movies

    def test_doс_viewed_movies_status_code(self, get_url, login_data):
        self.client.login(**login_data['user'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_doс_viewed_movies_add(self, login_data):
        self.client.login(**login_data['user'])
        user = get_user_model().objects.get(
            email=login_data['user']['username'],
        )
        movies_count = self.model.objects.count()
        response = self.client.get(
            reverse('movies-deleteorcreate-viewed')
        )
        if not user.viewed.count():
            assert user.viewed.count() == 0
        else:
            assert user.viewed.count() == movies_count
