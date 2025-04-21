"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.sitemaps.views import sitemap
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)

from apps.movies.sitemaps import MoviesSitemap
from api.accounts_v1 import views


sitemaps = {
    'movies': MoviesSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("apps.accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls',)),
    path('directors/', include('apps.directors.urls')),
    path('movies/', include('apps.movies.urls')),
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path('api/movies_v1/', include('api.movies_v1.urls')),
    path('api/directors_v1/', include('api.directors_v1.urls')),
    path('api/accounts_v1/', include('api.accounts_v1.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    # Auth
    path(
        'api/token/',
        views.CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        views.CustomTokenRefreshView.as_view(),
        name='token_refresh'
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
) + debug_toolbar_urls()
