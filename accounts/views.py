from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, LoginForm
from tweet.models import Tweet

User = get_user_model()


class IndexView(TemplateView):
    template_name = "accounts/index.html"


class HomeView(LoginRequiredMixin, ListView):
    template_name = "accounts/home.html"
    context_object_name = "tweet_list"

    queryset = Tweet.objects.all().select_related("user")


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class UserLogoutView(LogoutView):
    pass
