from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from config import settings
from tweet.models import Tweet
from .models import Profile, FriendShip
from django.contrib.messages import get_messages


User = get_user_model()


class SignUpTests(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_signup_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_successful_signup_post(self):
        self.data = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "testpass1",
            "password2": "testpass1",
        }

        response = self.client.post(self.url, data=self.data)
        self.assertTrue(User.objects.exists())
        self.assertRedirects(
            response, reverse(settings.LOGIN_REDIRECT_URL), target_status_code=302
        )

    def test_invalid_signup_redirect_same_page_post(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)
        form = response.context.get("form")
        self.assertTrue(form.errors)
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_empty_username(self):
        data_empty_username = {
            "username": "",
            "email": "test@gmail.com",
            "password1": "testpass1",
            "password2": "testpass1",
        }
        response = self.client.post(self.url, data_empty_username)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        data_empty_password = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data_empty_password)
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user("existing_user", "", "testpass1")
        data_duplicated_user = {
            "username": "existing_user",
            "email": "test@gmail.com",
            "password1": "testpass1",
            "password2": "testpass1",
        }
        response = self.client.post(self.url, data_duplicated_user)
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_password_too_short_password(self):
        data_too_short_password = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "jpo34",
            "password2": "jpo34",
        }
        response = self.client.post(self.url, data_too_short_password)
        self.assertFormError(
            response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。"
        )

    def test_failure_post_with_password_similar_to_username(self):
        data_password_similar_to_username = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "new_user",
            "password2": "new_user",
        }
        response = self.client.post(self.url, data_password_similar_to_username)
        self.assertFormError(response, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        data_only_numbers_password = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "57892709",
            "password2": "57892709",
        }
        response = self.client.post(self.url, data_only_numbers_password)
        self.assertFormError(response, "form", "password2", "このパスワードは数字しか使われていません。")

    def test_failure_post_with_mismatch_password(self):
        data_mismatch_password = {
            "username": "new_user",
            "email": "test@gmail.com",
            "password1": "testpass1",
            "password2": "testpass2",
        }
        response = self.client.post(self.url, data_mismatch_password)
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")

    def test_failure_post_with_empty_email(self):
        data_empty_email = {
            "username": "new_user",
            "email": "",
            "password1": "testpass1",
            "password2": "testpass1",
        }
        response = self.client.post(self.url, data_empty_email)
        self.assertFormError(response, "form", "email", "このフィールドは必須です。")

    def test_failure_post_with_invalid_email(self):
        data_invalid_email = {
            "username": "new_user",
            "email": "abc",
            "password1": "testpass1",
            "password2": "testpass1",
        }
        response = self.client.post(self.url, data_invalid_email)
        self.assertFormError(response, "form", "email", "有効なメールアドレスを入力してください。")


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("login_user", "", "testpass")
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "login_user",
            "password": "testpass",
        }
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        self.assertEquals(response.status_code, 302)

    def test_failure_post_with_not_exists_user(self):
        data_not_exists_user = {
            "username": "not_exists_user",
            "password": "testpass",
        }
        response = self.client.post(self.url, data_not_exists_user)
        self.assertEquals(
            response.context.get("form").errors["__all__"],
            ["正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"],
        )
        self.assertEquals(response.status_code, 200)

    def test_failure_post_with_empty_password(self):
        data_not_exists_user = {
            "username": "login_user",
            "password": "",
        }

        response = self.client.post(self.url, data_not_exists_user)
        self.assertEquals(
            response.context.get("form").errors["password"], ["このフィールドは必須です。"]
        )
        self.assertEquals(response.status_code, 200)


class LogoutTest(TestCase):
    def setUp(self):
        User.objects.create_user("login_user", "", "testpass")
        self.client.login(username="login_pass", password="testpass")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@email.com", password="test_pass"
        )
        self.client.login(username="test_user", password="test_pass")
        self.url = reverse("accounts:home")
        Tweet.objects.create(
            user=self.user,
            content="test_tweet1",
        )
        Tweet.objects.create(
            user=self.user,
            content="test_tweet2",
        )

    def test_sccess_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")
        self.assertQuerysetEqual(
            response.context["tweet_list"], Tweet.objects.order_by("-created_at")
        )


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@email.com", password="test_pass"
        )
        self.client.login(username="test_user", password="test_pass")

    def test_success_get(self):
        user = User.objects.get(username="test_user")
        response_get = self.client.get(
            reverse("accounts:user_profile", kwargs={"pk": user.pk})
        )
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "accounts/profile.html")
        self.assertQuerysetEqual(
            response_get.context["tweet_list"], Tweet.objects.filter(user=user).order_by("created_at"),
        )

    def test_failure_get_with_not_exists_user(self):
        response = self.client.get(reverse("accounts:user_profile", kwargs={"pk": 500}))
        self.assertEqual(response.status_code, 404)


class UserProfileEditView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", email="test@email.com", password="test_pass"
        )
        self.client.login(username="test_user", password="test_pass")

    def test_success_get(self):
        user = User.objects.get(username="test_user")
        url = reverse("accounts:user_profile_edit", kwargs={"pk": user.pk})
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "accounts/profile_edit.html")

    def test_success_post(self):
        data_post = {
            "comment": "test comment",
        }
        user = User.objects.get(username="test_user")
        response_post = self.client.post(
            reverse("accounts:user_profile_edit", kwargs={"pk": user.pk}), data_post
        )
        self.assertRedirects(
            response_post,
            reverse("accounts:user_profile", kwargs={"pk": user.pk}),
            status_code=302,
            target_status_code=200,
        )
        user_object = Profile.objects.get(comment="test comment")
        self.assertEqual(user_object.comment, data_post["comment"])

    def test_failure_post_with_not_exists_user(self):
        response = self.client.get(
            reverse("accounts:user_profile", kwargs={"pk": 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_failure_post_with_incorrect_user(self):
        incorrect_user_data = {"comment": "test comment"}
        User.objects.create_user(
            username="imitation", email="test@email.com", password="testpass"
        )
        incorrect_user = User.objects.get(username="imitation")
        response_incorrect = self.client.post(
            reverse("accounts:user_profile_edit", kwargs={"pk": incorrect_user.pk}), incorrect_user_data,
        )
        self.assertEquals(response_incorrect.status_code, 403)
        self.assertFalse(
            Profile.objects.filter(comment="test comment").exists()
        )

class FollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test_user1", email="test1@email.com", password="test_pass1"
        )
        self.user2 = User.objects.create_user(
            username="test_user2", email="test2@email.com", password="test_pass2"
        )
        self.client.login(username="test_user1", password="test_pass1")

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test_user2"})
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test_user3"})
        )
        self.assertEqual(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "ユーザーが見つかりません。")
        self.assertEquals(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_self(self):
        response = self.client.post(
            reverse("accounts:follow", kwargs={"username": "test_user1"})
        )
        self.assertEquals(response.status_code, 302)
        messages =list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "自分自身はフォローできません。")
        self.assertEqual(FriendShip.objects.filter(follower=self.user1).count(), 0)

    
class UnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="test_user1", email="test1@email.com", password="test_pass1"
        )
        self.user2 = User.objects.create_user(
            username="test_user2", email="test2@email.com", password="test_pass2"
        )
        self.client.login(username="test_user1", password="test_pass1")
        FriendShip.objects.create(following=self.user2, follower=self.user1)

    def test_success_post(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test_user2"}),
        )
        self.assertRedirects(
            response,
            reverse("accounts:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEquals(FriendShip.objects.filter(follower=self.user1).count(), 0)

    def test_failure_post_with_not_exist_user(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test_user3"})
        )
        self.assertEquals(response.status_code, 404)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "ユーザーが見つかりません。")
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)

    def test_failure_post_with_incrrect_user(self):
        response = self.client.post(
            reverse("accounts:unfollow", kwargs={"username": "test_user1"})
        )
        self.assertEquals(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, "自分自身のフォローは解除できません。")
        self.assertTrue(FriendShip.objects.filter(follower=self.user1).exists)


class FollowingListView(TestCase):

    def test_success_get(self):
        self.user1 = User.objects.create_user(
            username="test_user1", email="test1@email.com", password="test_pass1"
        )
        self.client.login(username="test_user1", password="test_pass1")
        user = User.objects.get(username= "test_user1")
        response = self.client.get(reverse("accounts:following_list", kwargs={"pk": user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")


class FollowerListView(TestCase):
    def test_success_get(self):
        self.user1 = User.objects.create_user(
            username="test_user1", email="test1@email.com", password="test_pass1"
        )
        self.client.login(username="test_user1", password="test_pass1")
        user = User.objects.get(username= "test_user1")
        response = self.client.get(reverse("accounts:follower_list", kwargs={"pk": user.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
