from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404

from .models import Tweet
from .forms import TweetForm


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweet/tweet_detail.html"
    context_object_name = "tweet"


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweet/tweet_create.html"
    form_class = TweetForm
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweet/tweet_delete.html"
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        if Tweet.objects.filter(pk=self.kwargs["pk"]).exists():
            current_user = self.request.user
            tweet_user = Tweet.objects.get(pk=self.kwargs["pk"]).user
            return current_user.pk == tweet_user.pk
        else:
            raise Http404
