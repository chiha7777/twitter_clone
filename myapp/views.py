from django.shortcuts import render
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy

from .forms import SignUpForm

class IndexView(TemplateView):
  template_name = "myapp/index.html"

class HomeView(TemplateView):
  template_name = "myapp/home.html"

class SignUpView(CreateView):
  form_class = SignUpForm
  template_name = "myapp/signup.html"
  success_url = reverse_lazy("myapp:home")

  def form_valid(self, form):
      user = form.save()
      login(self.request, user)
      self.object = user
      return HttpResponseRedirect(self.get_success_url())
