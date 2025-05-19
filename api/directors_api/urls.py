from django.urls import path

from api.directors_api import views

urlpatterns = [
    path(
        'create/',
        views.CreateDirectorsAPIView.as_view(),
        name='api-directors-create'
    ),
    path('delete/<slug:pk>/',
         views.DeleteDirectorsAPIView.as_view(),
         name='api-directors-delete'
         )
]