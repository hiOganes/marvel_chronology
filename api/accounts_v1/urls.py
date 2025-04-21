from django.urls import path

from api.accounts_v1 import views

urlpatterns = [
    path('signup/', views.SignUpAPIView.as_view(), name='accounts_v1-signup'),
]