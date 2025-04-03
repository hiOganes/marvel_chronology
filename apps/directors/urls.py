from django.urls import path

from apps.directors import views


urlpatterns = [
    path(
        'create/',
        views.CreateDirectorsView.as_view(),
        name='directors-create'
    ),
    path(
        'created/',
        views.CreatedDirectorsView.as_view(),
        name='directors-created'
    ),
]