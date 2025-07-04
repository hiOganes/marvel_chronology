from django.test import TestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.movies.models import Movies
from api.movies_api.data_tests import new_movie, update_movie


class TestCreateMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.url = reverse('movies-create')
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]

    def test_create_movies_status_code_get_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_movies_status_code_get_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_movies_status_code_get_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_movies_status_code_post_anonymous(self):
        response = self.client.post(self.url, data=new_movie())
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_movies_status_code_post_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=new_movie())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_movies_status_code_post_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data=new_movie())
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_movies_status_code_post_invalid_data(self):
        edit_movie = new_movie()
        edit_movie['position'] = 'string'
        before = Movies.objects.count()
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data=edit_movie)
        after = Movies.objects.count()
        self.assertEqual(before, after)

    def test_create_movies_status_code_post_empty_data(self):
        before = Movies.objects.count()
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data={})
        after = Movies.objects.count()
        self.assertEqual(before, after)


class TestMoviesCreatedView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.url = reverse('movies-created')
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]

    def test_movies_created_status_code(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movies_created_template(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'movies/created.html')


class TestDeleteMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.movie = self.model.objects.all()[0]
        self.url = reverse('movies-delete', kwargs={'pk': self.movie.pk})
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]

    def test_delete_movies_status_code_get_anonymous(self):
        response = self.client.get(self.url, kwargs={'pk': self.movie.pk})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_movies_status_code_get_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url, kwargs={'pk': self.movie.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_movies_status_code_get_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url, kwargs={'pk': self.movie.pk})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_delete_movies_count_get(self):
        self.client.force_login(self.superuser)
        movies_before = Movies.objects.count()
        response = self.client.get(self.url, kwargs={'pk': self.movie.pk})
        movies_after = Movies.objects.count()
        self.assertTrue(movies_before > movies_after)


class TestDeleteOrCreateViewedView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.url = reverse('movies-deleteorcreate-viewed')
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]

    def test_doс_viewed_movies(self):
        self.client.force_login(self.superuser)
        movies_count = self.model.objects.count()
        response = self.client.get(self.url)
        self.assertIn(self.superuser.viewed.count(), [movies_count, 0])


class TestDetailMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.movie = self.model.objects.all()[0]
        self.url = reverse('movies-detail', kwargs={'pk': self.movie.pk})

    def test_detail_movies_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_movies_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'movies/detail.html')


class TestListMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('movies-list')

    def test_list_movies_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_movies_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'movies/list.html')

    def test_list_movies_pagination(self):
        response = self.client.get(self.url)
        self.assertTrue(len(response.context['pages_movies']) == 10)


class TestUpdateMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.movie = self.model.objects.all()[0]
        self.url = reverse('movies-update', kwargs={'pk': self.movie.pk})
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]

    def test_update_movies_status_code_get_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_movies_status_code_post_anonymous(self):
        response = self.client.post(self.url, data=update_movie)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_movies_status_code_get_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_movies_status_code_post_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, data=update_movie)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_movies_status_code_get_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_movies_status_code_post_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(self.url, data=update_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestViewedMoviesView(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        self.model = Movies
        self.movie = self.model.objects.all()[0]
        self.url = reverse('movies-viewed', kwargs={'pk': self.movie.pk})
        self.superuser = get_user_model().objects.filter(is_superuser=True)[0]
        self.user = get_user_model().objects.filter(is_superuser=False)[0]

    def test_viewed_movies_status_code(self):
        self.client.force_login(self.superuser)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_viewed_movies_add(self):
        self.client.force_login(self.superuser)
        viewed_before = self.superuser.viewed.count()
        response = self.client.get(self.url)
        viewed_after = self.superuser.viewed.count()
        self.assertTrue(viewed_before < viewed_after)
        response = self.client.get(self.url)
        viewed_after = self.user.viewed.count()
        self.assertEqual(viewed_before, viewed_after)
