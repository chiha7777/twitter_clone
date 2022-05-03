from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.urls import resolve, reverse


User = get_user_model()

class SignUpTests(TestCase):
    def setUp(self):
        self.url = reverse('accounts:signup')
  
    def test_success_signup_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_successful_signup_post(self):
        data = {
          'username' : 'new_user',
          'email' : 'test@gmail.com',
          'password1': 'testpass1',
          'password2': 'testpass1',
        }

        post_response = self.client.post(self.url, data=data)
        self.assertTrue(User.objects.exists())
    
    def test_invalid_signup_post(self):
        response = self.client.post(self.url,{})
        self.assertEquals(response.status_code, 200)
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertFalse(User.objects.exists())

    def test_failure_post_with_password_too_short_password(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : 'test@gmail.com', 'password1' : 'jpo34', 'password2' : 'jpo34'})
        self.assertFormError(response, 'form', 'password2', 'このパスワードは短すぎます。最低 8 文字以上必要です。')

    def test_failure_post_with_password_similar_to_username(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : 'test@gmail.com', 'password1' : 'new_user', 'password2' : 'new_user'})
        self.assertFormError(response, 'form', 'password2', 'このパスワードは ユーザー名 と似すぎています。')

    def test_failure_post_with_only_numbers_password(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : 'test@gmail.com', 'password1' : '57892709', 'password2' : '57892709'})
        self.assertFormError(response, 'form', 'password2', 'このパスワードは数字しか使われていません。')
  
    def test_failure_post_with_mismatch_password(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : 'test@gmail.com', 'password1' : 'testpass1', 'password2' : 'testpass2'})
        self.assertFormError(response, 'form', 'password2', '確認用パスワードが一致しません。')

    def test_failure_post_with_empty_email(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : '', 'password1' : 'testpass1', 'password2' : 'testpass1'})
        self.assertFormError(response, 'form', 'email', 'メールアドレスを入力してください。')

    def test_failure_post_with_invalid_email(self):
        response = self.client.post(self.url, {'username' : 'new_user', 'email' : 'abc', 'password1' : 'testpass1', 'password2' : 'testpass1'})
        self.assertFormError(response, 'form', 'email', '有効なメールアドレスを入力してください。')
