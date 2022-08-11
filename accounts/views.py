from django.views.generic import TemplateView, CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)

from .forms import SignUpForm
from .forms import LoginForm

User = get_user_model()

class IndexView(TemplateView):
    template_name = "accounts/index.html"

class HomeView(TemplateView):
    template_name = "accounts/home.html"

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class Login(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

class Logout(LogoutView):
    pass
