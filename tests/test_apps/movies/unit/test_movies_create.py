from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status
from pytest_django import asserts

from apps.movies.models import Movies
from apps.directors.models import Directors


@pytest.fixture
def new_movie():
    data = {
        'position': 1,
        'title_ru': 'Фильм',
        'title_en': 'Film',
        'release_date': datetime.now(),
        'timing': 100,
        'director_id': Directors.objects.all()[0],
        'trailer': 'https://www.youtube.com/watch?v=FxTlOl03x9c',
        'description': 'description',
        'poster': 'posters/2025/04/09/3840x.webp',
        'content': 'MOVIE'
    }
    return data


@pytest.mark.django_db()
class TestCreateMoviesView:
    client = Client()
    model = Movies
    url = reverse('movies-create')

    def test_create_movies_status_code_get(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_302_FOUND

    def test_create_movies_status_code_post(self, new_movie):
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_302_FOUND

    def test_create_movies_status_code_get_user(self):
        self.client.login(username='ogksandr@gmail.com', password='1234')
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_movies_status_code_post_user(self, new_movie):
        self.client.login(username='ogksandr@gmail.com', password='1234')
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_movies_status_code_get_superuser(self):
        self.client.login(username='soft.oganes@gmail.com', password='1234')
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_movies_status_code_post_superuser(self, new_movie):
        self.client.login(username='soft.oganes@gmail.com', password='1234')
        response = self.client.post(self.url, data=new_movie)
        assert response.status_code == status.HTTP_200_OK
