from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin

from apps.directors.forms import DirectorsForm
from apps.directors.models import Directors


class CreateDirectorsView(PermissionRequiredMixin, View):
    template_name = 'directors/create.html'
    form_class = DirectorsForm
    model = Directors
    permission_required = "directors.add_directors"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.model.objects.create(**form.cleaned_data)
            return redirect('directors-created')
        return render(request, self.template_name, {'errors': form.errors})


class CreatedDirectorsView(PermissionRequiredMixin, View):
    template_name = 'directors/created.html'
    permission_required = "directors.add_directors"

    def get(self, request):
        return render(request, self.template_name)