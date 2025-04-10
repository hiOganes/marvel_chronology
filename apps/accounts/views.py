from django.urls import path, reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import CreateView

from apps.accounts.forms import UserForm


def custom_logout(request):
    logout(request)
    return redirect('movies-list')


class SignUpView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'