from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.accounts.models import User
from api.accounts_api.serializers import SignUpSerializer


tags = ['AuthJWT']


class SignUpAPIView(APIView):
    model = User
    serializer_class = SignUpSerializer

    @extend_schema(
        tags=tags,
        summary='This endpoint create a new user',
        request=SignUpSerializer,
        responses={201: TokenObtainPairSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.model(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                is_active=True,
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)
            if not user.is_staff:
                refresh.payload.update({'group': 'users'})
            auth_keys = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data=auth_keys, status=status.HTTP_201_CREATED)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    tags=tags,
    summary='This endpoint receives the refresh and access token',
    request=TokenObtainPairSerializer,
    responses={200: TokenObtainPairSerializer}
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=tags,
    summary='This endpoint returns a new access token.',
    request=TokenRefreshSerializer,
    responses={200: TokenRefreshSerializer}
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

