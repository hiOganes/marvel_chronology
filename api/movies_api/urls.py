from django.urls import path

from api.movies_api import views

urlpatterns = [
    path('list/', views.ListMoviesAPIView.as_view(), name='api-movies-list'),
    path(
        'detail/<slug:pk>/',
        views.DetailMoviesAPIView.as_view(),
        name='api-movies-detail'
    ),
    path('viewed/', views.ViewedAPIView.as_view(), name='api-viewed-status')
]