from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('logout/', views.custom_logout, name='custom-logout'),
    path('signup/', views.SignUpView.as_view(), name='signup')
]