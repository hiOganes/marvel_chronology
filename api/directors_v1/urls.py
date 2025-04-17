from django.urls import path

from api.directors_v1 import views

urlpatterns = [
    path(
        'create/',
        views.CreateDirectorsAPIView.as_view(),
        name='api-directors-create'
    ),
    path(''
         'delete/<slug:id>/',
         views.DeleteDirectorsAPIView.as_view(),
         name='api-directors-delete'
         )
]