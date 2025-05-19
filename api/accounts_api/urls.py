from django.urls import path

from api.accounts_api import views

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='accounts_api-signup'),
]