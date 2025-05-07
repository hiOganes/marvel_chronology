from rest_framework.test import (
    APIRequestFactory, force_authenticate, APITestCase
)
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from api.accounts_v1 import views
from api.accounts_v1.data_tests import user_sign_up, user_sign_in, user_invalid


class TestSignUpAPIView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.url = reverse('accounts_v1-signup')
        self.view = views.SignUpAPIView.as_view()
        self.factory = APIRequestFactory()

    def test_sign_up(self):
        users_before = get_user_model().objects.count()
        request = self.factory.post(self.url, user_sign_up)
        response = self.view(request)
        users_after = get_user_model().objects.count()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(users_before < users_after)

    def test_sign_up_invalid_email(self):
        user_sign_up['email'] = 'invalid.inv'
        request = self.factory.post(self.url, user_sign_up)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_invalid_password(self):
        user_sign_up['password'] = '12345678'
        request = self.factory.post(self.url, user_sign_up)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_sign_up['password'] = 'abcdefgh'
        request = self.factory.post(self.url, user_sign_up)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_empty_data(self):
        request = self.factory.post(self.url, {})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestCustomTokenObtainPairView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.url = reverse('token_obtain_pair')
        self.view = views.CustomTokenObtainPairView.as_view()
        self.factory = APIRequestFactory()
        get_user_model().objects.create_user(**user_sign_up)

    def test_get_tokens(self):
        request = self.factory.post(self.url, user_sign_in)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_tokens_invalid_user(self):
        request = self.factory.post(self.url, user_invalid)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_tokens_missing_user(self):
        request = self.factory.post(self.url, {})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestCustomTokenRefreshView(APITestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.url = reverse('token_refresh')
        self.view = views.CustomTokenRefreshView.as_view()
        self.factory = APIRequestFactory()
        self.tokens = views.SignUpAPIView.as_view()(
            self.factory.post(reverse('accounts_v1-signup'), user_sign_up)
        ).data

    def test_get_refresh_token(self):
        request = self.factory.post(
            self.url, {'refresh': self.tokens['refresh']}
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_refresh_token_invalid_data(self):
        request = self.factory.post(
            self.url, {'refresh': 'invalid_token'}
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_refresh_token_missing_data(self):
        request = self.factory.post(
            self.url, {}
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
