from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
)
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect

from .models import Profile, FriendShip
from .forms import ProfileForm, SignUpForm, LoginForm
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


class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile.html"
    model = Profile

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        user = self.object.user
        ctx["tweet_list"] = Tweet.objects.select_related("user").filter(user=user)
        ctx["following_count"] = FriendShip.objects.filter(follower=user).count()
        ctx["follower_count"] = FriendShip.objects.filter(following=user).count()
        ctx["has_following_connection"] = (
            FriendShip.objects.select_related("follower", "following")
            .filter(follower=self.request.user, following=user)
            .exists()
        )

        return ctx


class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "accounts/profile_edit.html"
    model = Profile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse("accounts:user_profile", kwargs={"pk": self.object.pk})

    def test_func(self):
        current_user = self.request.user
        return current_user.pk == self.kwargs["pk"]


class FollowView(LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            following = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.error(request, "ユーザーが見つかりません。")
            raise Http404
        if follower == following:
            messages.error(request, "自分自身はフォローできません。")
        elif FriendShip.objects.filter(follower=follower, following=following).exists():
            messages.error(request, "既にフォローしています。")
        else:
            FriendShip.objects.get_or_create(follower=follower, following=following)
            messages.success(request, "フォローしました。")
        return HttpResponseRedirect(reverse_lazy("accounts:home"))


class UnFollowView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        follower = self.request.user
        try:
            following = User.objects.get(username=self.kwargs["username"])
        except User.DoesNotExist:
            messages.error(request, "ユーザーが見つかりません。")
            raise Http404

        if follower == following:
            messages.error(request, "自分自身のフォローは解除できません。")
            return render(request, "accounts/home.html", status=200)
        elif FriendShip.objects.filter(follower=follower, following=following).exists():
            FriendShip.objects.filter(follower=follower, following=following).delete()
            messages.success(request, "フォローを解除しました。")
        else:
            messages.error(request, "元々フォローしていません。")
        return HttpResponseRedirect(reverse_lazy("accounts:home"))


class FollowerListView(LoginRequiredMixin, DetailView):
    template_name = "accounts/follower_list.html"
    model = Profile

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_context_data(self, *args, **kwargs):
        user = self.object.user
        ctx = super().get_context_data(*args, **kwargs)
        ctx["follower_list"] = FriendShip.objects.select_related("follower").filter(
            following=user
        )
        return ctx


class FollowingListView(LoginRequiredMixin, DetailView):
    template_name = "accounts/following_list.html"
    model = Profile

    def get_queryset(self):
        return super().get_queryset().select_related("user")

    def get_context_data(self, *args, **kwargs):
        user = self.object.user
        ctx = super().get_context_data(*args, **kwargs)
        ctx["following_list"] = FriendShip.objects.select_related("following").filter(
            follower=user
        )
        return ctx
