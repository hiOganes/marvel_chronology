from django.urls import path

from api.movies_v1 import views

urlpatterns = [
    path('list/', views.ListMoviesAPIView.as_view(), name='api-movies-list'),
]