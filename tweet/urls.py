from django.urls import path
from . import views

app_name = "tweet"

urlpatterns = [
    path("<int:pk>/", views.TweetDetailView.as_view(), name="detail"),
    path("create/", views.TweetCreateView.as_view(), name="create"),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name="delete"),
]
