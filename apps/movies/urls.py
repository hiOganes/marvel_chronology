from django.urls import path

from apps.movies import views

urlpatterns = [
    path('create/', views.CreateMoviesView.as_view(), name='movies-create'),
    path('created/', views.CreatedMoviesView.as_view(), name='movies-created'),
    path('list/', views.ListMoviesView.as_view(), name='movies-list'),
    path(
        'detail/<slug:pk>/',
        views.DetailMoviesView.as_view(),
        name='movies-detail'
    ),
    path(
        'update/<slug:pk>/',
        views.UpdateMoviesView.as_view(),
        name='movies-update'
    ),
    path(
        'delete/<slug:pk>/',
        views.DeleteMoviesView.as_view(),
        name='movies-delete'
    ),
    path('viewed/<slug:pk>/', views.ViewedView.as_view(), name='movies-viewed'),
    path('viewed-deleteorcreate/', views.DeleteOrCreateViewedView.as_view(), name='movies-deleteorcreate-viewed'),
]