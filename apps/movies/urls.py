from django.urls import path

from apps.movies import views

urlpatterns = [
    path('create/', views.CreateMoviesView.as_view(), name='movies-create'),
    path('created/', views.CreatedMoviesView.as_view(), name='movies-created'),
    path('list/', views.ListMoviesView.as_view(), name='movies-list'),
]