from django.test import TestCase
from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.db.utils import IntegrityError
from django.urls import resolve, reverce

from .models import Relationship
from .views import signup


class TestSignUpView(TestCase):
  def setUp(self):
    self.user = reverse('accounts:signup')
  
  def test_signup_get(self):
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
