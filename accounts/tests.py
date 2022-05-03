from django.test import TestCase
from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.db.utils import IntegrityError
from django.urls import resolve, reverse


from .views import singup

User = get_user_model()

class SignUpTests(TestCase):
  def setUp(self):
    self.url = reverse('accounts:singup')
  
  def test_success_signup_get(self):
    response = self.client.get(self.url)
    self.assertEquals(response.status_code, 200)

  def test_successful_signup_post(sefl):
    data = {
      'username' : 'new_user',
      'password1': 'testpass1',
      'password2': 'testpass1',
    }

    post_response = self.client.post(self.url, data=data)
    mypostlist_url = reverse('tweet:mypostlist')
    self.assertRedirects(post_response, mypostlist_url)
    self.assertTrue(User.objects.exists())
    get_response = self.client.get(mypostlist_url)
    user = get_response.context.get('user')
    self.assertTrue(user.is_authenticated)

  def test_invalid_signup_post(self):
    response = self.client.post(self.url,{})
    self.assertEquals(response.status_cade, 200)
    form = response.context.get('form')
    self.assertTrue(form.errors)
    self.assertFalse(User.objects.exits())

  def test_failure_post_with_password_too_short_password(self):
    response = self.client.post(self.url, {'username' : 'new_user', 'password1' : 'jpo34', 'password2' : 'jpo34'})
    self.assertFormError(response,'form', 'password2', 'このパスワードは短すぎます。８文字以上で入力してください。')

  def test_failure_post_with_password_similar_to_username(self):
    response = self.client.post(self.url, {'username' : 'new_user', 'password1' : 'new_user', 'password2' : 'new_user'})
    self.asserFormError(response, 'form', 'password2', 'ユーザーネームとパスワードが違うものにしてください。')

  def test_failure_post_with_only_numbers_password(self):
    response = self.client.post(self.url, {'username' : 'new_user', 'password1' : '57892709', 'password2' : '57892709'})
    self.asserFormError(response, 'form', 'password2', 'パスワードは英語と数字を組み合わせてください。')
  
  def test_failure_post_with_mismatch_password(self):
    response = self.client.post(self.url, {'username' : 'new_user', 'password1' : 'testpass1', 'password2' : 'testpass2'})
    self.asserFormError(response, 'form', '確認用パスワードが一致しません。')
