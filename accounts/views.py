from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
<<<<<<< HEAD
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from .forms import SignUpForm, LoginForm
from tweet.models import Tweet
=======
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import(LoginView, LogoutView)

from .forms import SignUpForm
from .forms import LoginForm
>>>>>>> parent of 392aa56 (changed test.py and views.py)

User = get_user_model()

class IndexView(TemplateView):
    template_name = "accounts/index.html"

<<<<<<< HEAD

class HomeView(LoginRequiredMixin, ListView):
=======
class HomeView(TemplateView):
>>>>>>> parent of 392aa56 (changed test.py and views.py)
    template_name = "accounts/home.html"
    context_object_name = "tweet_list"

    def get_queryset(self):
        return Tweet.objects.all().select_related("user")

    def tweet_detail(request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        return render(request, "tweet/tweet_detail.html", {"tweet": tweet})

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

<<<<<<< HEAD

class UserLoginView(LoginView):
=======
class Login(LoginView):
>>>>>>> parent of 392aa56 (changed test.py and views.py)
    form_class = LoginForm
    template_name = 'accounts/login.html'

class UserLogoutView(LogoutView):
    pass
