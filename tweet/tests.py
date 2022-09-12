from django.test import TestCase
from django.urls import reverse

from .models import Tweet
from accounts.models import User


class TestTweetCreateView(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="test_user",
            email="test@email.com",
            password="test_pass",
        )
        self.client.login(username="test_user", password="test_pass")
        self.url = reverse("tweet:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweet/tweet_create.html")

    def test_success_post(self):
        data = {"content": "test_tweet"}
        response = self.client.post(self.url, data)
        self.assertTrue(Tweet.objects.exists())
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )

    def test_failure_post_with_empty_content(self):
        data_empty_content = {"content": ""}
        response = self.client.post(self.url, data_empty_content)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "このフィールドは必須です。",
        )
        self.assertFalse(Tweet.objects.exists())

    def test_failure_post_with_too_long_content(self):
        data_too_long_content = {"content": "a" * 210}
        response = self.client.post(self.url, data_too_long_content)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "この値は 200 文字以下でなければなりません( "
            + str(len(data_too_long_content["content"]))
            + " 文字になっています)。",
        )
        self.assertFalse(Tweet.objects.exists())


class TestDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@email.com",
            password="test_pass",
        )
        self.client.login(username="test_user", password="test_pass")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")

    def test_success_get(self):
        response = self.client.get(
            reverse("tweet:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweet/tweet_detail.html")
        self.assertEqual(self.tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@email.com",
            password="test_pass",
        )
        self.user2 = User.objects.create_user(
            username="test_user2",
            email="test2@email.com",
            password="test_pass2",
        )
        self.client.login(username="test_user", password="test_pass")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="test_tweet2")

    def test_success_post(self):
        response = self.client.post(
            reverse("tweet:delete", kwargs={"pk": self.tweet.pk})
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )

    def test_failure_post_with_noto_exist_tweet(self):
        response = self.client.post(reverse("tweet:delete", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.exists())

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(
            reverse("tweet:delete", kwargs={"pk": self.tweet2.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.exists())
